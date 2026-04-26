"""
LoRATrainingPipeline: QLoRA + SFTTrainer production pipeline with merge-and-unload.
Input:  LoRAConfig (base_model, rank, alpha, dropout, target_modules, use_4bit)
Output: trained adapter saved to output_dir; merged model at output_dir/merged
"""
import logging
from dataclasses import dataclass, field
from typing import Optional
import torch
from datasets import Dataset
from peft import (
    LoraConfig, TaskType, get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    BitsAndBytesConfig, TrainingArguments,
)
from trl import SFTTrainer


@dataclass
class LoRAConfig:
    base_model: str
    rank: int = 16
    alpha: int = 16
    dropout: float = 0.05
    target_modules: list = field(default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"])
    use_4bit: bool = True
    max_length: int = 512
    batch_size: int = 2
    num_epochs: int = 3
    learning_rate: float = 2e-4
    output_dir: str = "./lora-output"


class LoRATrainingPipeline:
    def __init__(self, config: LoRAConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def prepare_model(self):
        if self.config.use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
            )
            model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model, quantization_config=bnb_config, device_map="auto"
            )
            model = prepare_model_for_kbit_training(model)  # MUST be before get_peft_model
        else:
            model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model, torch_dtype=torch.float16, device_map="auto"
            )

        lora_cfg = LoraConfig(
            r=self.config.rank, lora_alpha=self.config.alpha,
            lora_dropout=self.config.dropout, target_modules=self.config.target_modules,
            bias="none", task_type=TaskType.CAUSAL_LM,
        )
        model = get_peft_model(model, lora_cfg)
        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        if trainable == 0:
            raise ValueError("No trainable params — check target_modules")
        self.logger.info("Trainable params: %d", trainable)

        tokenizer = AutoTokenizer.from_pretrained(self.config.base_model)
        tokenizer.pad_token = tokenizer.eos_token
        self.model = model
        self.tokenizer = tokenizer

    def train(self, train_data: list, val_data: Optional[list] = None) -> dict:
        self.prepare_model()
        train_ds = Dataset.from_list(train_data)
        val_ds = Dataset.from_list(val_data) if val_data else None

        args = TrainingArguments(
            output_dir=self.config.output_dir, num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size, gradient_accumulation_steps=4,
            learning_rate=self.config.learning_rate, bf16=True, logging_steps=10,
            save_strategy="epoch",
            evaluation_strategy="epoch" if val_ds else "no",
            warmup_ratio=0.03, lr_scheduler_type="cosine",
            optim="paged_adamw_8bit" if self.config.use_4bit else "adamw_torch",
        )

        trainer = SFTTrainer(
            model=self.model, tokenizer=self.tokenizer,
            train_dataset=train_ds, eval_dataset=val_ds,
            args=args, max_seq_length=self.config.max_length,
        )
        trainer.train()
        self.model.save_pretrained(self.config.output_dir)
        self.tokenizer.save_pretrained(self.config.output_dir)
        return {"status": "completed", "output_dir": self.config.output_dir}

    def merge_and_export(self) -> str:
        from peft import PeftModel
        merged_dir = self.config.output_dir + "/merged"
        merged = self.model.merge_and_unload()
        merged.save_pretrained(merged_dir)
        self.tokenizer.save_pretrained(merged_dir)
        return merged_dir
