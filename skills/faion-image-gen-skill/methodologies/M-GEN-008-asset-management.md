# M-GEN-008: Asset Management

## Overview

AI asset management handles versioning, organizing, and retrieving generated content (images, videos, audio, models). Proper management enables reuse, collaboration, and cost optimization. Covers storage, metadata, search, and lifecycle.

**When to use:** Any project generating significant AI content, teams collaborating on AI assets, or production systems with generated media.

## Core Concepts

### 1. Asset Types

| Type | Formats | Storage Size | Lifecycle |
|------|---------|--------------|-----------|
| **Images** | PNG, JPEG, WebP | 100KB-10MB | Long-term |
| **Videos** | MP4, WebM | 10MB-1GB | Long-term |
| **Audio** | MP3, WAV | 1-50MB | Long-term |
| **Embeddings** | JSON, Binary | 1-100KB | Regenerable |
| **Models** | GGUF, Safetensors | 1-100GB | Versioned |
| **Prompts** | Text, JSON | <1KB | Versioned |

### 2. Asset Lifecycle

```
Create → Store → Index → Search → Use → Archive/Delete
   ↓        ↓       ↓        ↓      ↓         ↓
Generate  Upload  Metadata  Query  Download  Cleanup
          Hash    Tags      Filter Render    Expire
```

### 3. Metadata Schema

```json
{
  "id": "asset_abc123",
  "type": "image",
  "format": "png",
  "size_bytes": 1234567,
  "dimensions": {"width": 1024, "height": 1024},
  "created_at": "2024-01-15T10:30:00Z",
  "created_by": "user_xyz",
  "generation": {
    "model": "dall-e-3",
    "prompt": "A serene mountain landscape...",
    "seed": 12345,
    "parameters": {"quality": "hd", "style": "vivid"}
  },
  "tags": ["landscape", "mountain", "nature"],
  "project": "marketing-campaign-q1",
  "status": "active",
  "versions": [
    {"version": 1, "path": "...", "created_at": "..."}
  ],
  "usage": {
    "download_count": 15,
    "last_accessed": "2024-01-20T14:00:00Z"
  }
}
```

## Best Practices

### 1. Implement Content-Addressable Storage

```python
import hashlib
from pathlib import Path
from datetime import datetime

class AssetStore:
    """Content-addressable asset storage."""

    def __init__(self, base_path: str, cloud_bucket: str = None):
        self.base_path = Path(base_path)
        self.cloud_bucket = cloud_bucket
        self.base_path.mkdir(parents=True, exist_ok=True)

    def store(self, content: bytes, metadata: dict) -> str:
        """Store asset with content-based addressing."""

        # Generate content hash
        content_hash = hashlib.sha256(content).hexdigest()

        # Determine file extension
        ext = metadata.get("format", "bin")

        # Create path structure: /ab/cd/abcd1234.png
        subdir = self.base_path / content_hash[:2] / content_hash[2:4]
        subdir.mkdir(parents=True, exist_ok=True)

        file_path = subdir / f"{content_hash}.{ext}"

        # Skip if exists (deduplication)
        if not file_path.exists():
            file_path.write_bytes(content)

            # Upload to cloud if configured
            if self.cloud_bucket:
                self._upload_to_cloud(file_path, content_hash)

        # Store metadata
        self._store_metadata(content_hash, metadata, file_path)

        return content_hash

    def get(self, asset_id: str) -> tuple[bytes, dict]:
        """Retrieve asset by ID."""
        metadata = self._get_metadata(asset_id)
        file_path = Path(metadata["path"])

        if not file_path.exists():
            # Try cloud fallback
            if self.cloud_bucket:
                content = self._download_from_cloud(asset_id)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(content)
            else:
                raise FileNotFoundError(f"Asset not found: {asset_id}")

        content = file_path.read_bytes()

        # Update access stats
        self._update_access_stats(asset_id)

        return content, metadata
```

### 2. Rich Metadata Indexing

```python
from elasticsearch import Elasticsearch

class AssetIndex:
    """Index assets for search and discovery."""

    def __init__(self, es_url: str):
        self.es = Elasticsearch(es_url)
        self._create_index()

    def _create_index(self):
        """Create Elasticsearch index with mappings."""

        self.es.indices.create(
            index="assets",
            ignore=400,  # Ignore if exists
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "type": {"type": "keyword"},
                        "format": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "created_by": {"type": "keyword"},
                        "prompt": {"type": "text", "analyzer": "english"},
                        "tags": {"type": "keyword"},
                        "project": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "embedding": {
                            "type": "dense_vector",
                            "dims": 512,
                            "index": True,
                            "similarity": "cosine"
                        }
                    }
                }
            }
        )

    def index_asset(self, asset_id: str, metadata: dict):
        """Index asset for search."""

        doc = {
            "id": asset_id,
            "type": metadata["type"],
            "format": metadata["format"],
            "created_at": metadata["created_at"],
            "created_by": metadata.get("created_by"),
            "prompt": metadata.get("generation", {}).get("prompt"),
            "tags": metadata.get("tags", []),
            "project": metadata.get("project"),
            "status": metadata.get("status", "active")
        }

        # Add embedding for visual similarity search
        if "embedding" in metadata:
            doc["embedding"] = metadata["embedding"]

        self.es.index(index="assets", id=asset_id, body=doc)

    def search(
        self,
        query: str = None,
        filters: dict = None,
        embedding: list = None,
        size: int = 20
    ) -> list:
        """Search assets."""

        must_clauses = []

        if query:
            must_clauses.append({
                "multi_match": {
                    "query": query,
                    "fields": ["prompt", "tags"]
                }
            })

        if filters:
            for field, value in filters.items():
                must_clauses.append({"term": {field: value}})

        body = {
            "query": {"bool": {"must": must_clauses}},
            "size": size
        }

        # Add vector similarity if embedding provided
        if embedding:
            body["knn"] = {
                "field": "embedding",
                "query_vector": embedding,
                "k": size,
                "num_candidates": size * 10
            }

        results = self.es.search(index="assets", body=body)
        return [hit["_source"] for hit in results["hits"]["hits"]]
```

### 3. Version Control for Assets

```python
from datetime import datetime
import copy

class AssetVersionControl:
    """Version control for AI assets."""

    def __init__(self, store: AssetStore, db):
        self.store = store
        self.db = db

    def create_version(
        self,
        asset_id: str,
        new_content: bytes,
        change_description: str
    ) -> dict:
        """Create new version of asset."""

        # Get current asset
        current = self.db.get_asset(asset_id)

        # Store new content
        new_hash = self.store.store(new_content, current["metadata"])

        # Create version record
        version = {
            "version_number": len(current.get("versions", [])) + 1,
            "content_hash": new_hash,
            "created_at": datetime.utcnow().isoformat(),
            "change_description": change_description,
            "previous_version": current.get("current_hash")
        }

        # Update asset record
        if "versions" not in current:
            current["versions"] = []
        current["versions"].append(version)
        current["current_hash"] = new_hash

        self.db.update_asset(asset_id, current)

        return version

    def get_version(self, asset_id: str, version_number: int = None) -> tuple:
        """Get specific version of asset."""

        asset = self.db.get_asset(asset_id)

        if version_number is None:
            # Get latest
            content_hash = asset["current_hash"]
        else:
            # Get specific version
            for v in asset["versions"]:
                if v["version_number"] == version_number:
                    content_hash = v["content_hash"]
                    break
            else:
                raise ValueError(f"Version {version_number} not found")

        content, metadata = self.store.get(content_hash)
        return content, metadata

    def list_versions(self, asset_id: str) -> list:
        """List all versions of asset."""
        asset = self.db.get_asset(asset_id)
        return asset.get("versions", [])
```

## Common Patterns

### Pattern 1: Cloud Storage Integration

```python
import boto3
from google.cloud import storage as gcs

class CloudAssetStorage:
    """Multi-cloud asset storage."""

    def __init__(self, provider: str, bucket: str):
        self.provider = provider
        self.bucket = bucket

        if provider == "s3":
            self.client = boto3.client("s3")
        elif provider == "gcs":
            self.client = gcs.Client()
            self.bucket_obj = self.client.bucket(bucket)

    def upload(self, local_path: str, remote_key: str, metadata: dict = None):
        """Upload asset to cloud."""

        if self.provider == "s3":
            extra_args = {}
            if metadata:
                extra_args["Metadata"] = {k: str(v) for k, v in metadata.items()}

            self.client.upload_file(
                local_path,
                self.bucket,
                remote_key,
                ExtraArgs=extra_args
            )

        elif self.provider == "gcs":
            blob = self.bucket_obj.blob(remote_key)
            if metadata:
                blob.metadata = metadata
            blob.upload_from_filename(local_path)

    def download(self, remote_key: str, local_path: str):
        """Download asset from cloud."""

        if self.provider == "s3":
            self.client.download_file(self.bucket, remote_key, local_path)

        elif self.provider == "gcs":
            blob = self.bucket_obj.blob(remote_key)
            blob.download_to_filename(local_path)

    def get_signed_url(self, remote_key: str, expiration: int = 3600) -> str:
        """Get temporary signed URL for asset."""

        if self.provider == "s3":
            return self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": remote_key},
                ExpiresIn=expiration
            )

        elif self.provider == "gcs":
            from datetime import timedelta
            blob = self.bucket_obj.blob(remote_key)
            return blob.generate_signed_url(expiration=timedelta(seconds=expiration))
```

### Pattern 2: Visual Similarity Search

```python
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

class VisualAssetSearch:
    """Search assets by visual similarity."""

    def __init__(self, asset_index: AssetIndex):
        self.index = asset_index
        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    def embed_image(self, image_path: str) -> list:
        """Generate embedding for image."""

        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            embedding = self.model.get_image_features(**inputs)

        return embedding[0].numpy().tolist()

    def find_similar(self, image_path: str, k: int = 10) -> list:
        """Find visually similar assets."""

        embedding = self.embed_image(image_path)
        return self.index.search(embedding=embedding, size=k)

    def find_by_text(self, query: str, k: int = 10) -> list:
        """Find assets matching text description."""

        inputs = self.processor(text=[query], return_tensors="pt", padding=True)

        with torch.no_grad():
            embedding = self.model.get_text_features(**inputs)

        return self.index.search(embedding=embedding[0].numpy().tolist(), size=k)

    def index_image(self, asset_id: str, image_path: str, metadata: dict):
        """Index image with embedding."""

        embedding = self.embed_image(image_path)
        metadata["embedding"] = embedding

        self.index.index_asset(asset_id, metadata)
```

### Pattern 3: Asset Collections

```python
class AssetCollection:
    """Organize assets into collections/projects."""

    def __init__(self, db):
        self.db = db

    def create_collection(
        self,
        name: str,
        description: str,
        owner: str
    ) -> str:
        """Create new collection."""

        collection = {
            "id": generate_id(),
            "name": name,
            "description": description,
            "owner": owner,
            "created_at": datetime.utcnow().isoformat(),
            "assets": [],
            "collaborators": []
        }

        self.db.insert("collections", collection)
        return collection["id"]

    def add_asset(self, collection_id: str, asset_id: str):
        """Add asset to collection."""

        collection = self.db.get("collections", collection_id)
        if asset_id not in collection["assets"]:
            collection["assets"].append(asset_id)
            self.db.update("collections", collection_id, collection)

    def get_assets(self, collection_id: str) -> list:
        """Get all assets in collection."""

        collection = self.db.get("collections", collection_id)
        return [self.db.get("assets", aid) for aid in collection["assets"]]

    def share_collection(self, collection_id: str, user_id: str, permission: str):
        """Share collection with user."""

        collection = self.db.get("collections", collection_id)
        collection["collaborators"].append({
            "user_id": user_id,
            "permission": permission  # "view", "edit", "admin"
        })
        self.db.update("collections", collection_id, collection)
```

### Pattern 4: Lifecycle Management

```python
from datetime import datetime, timedelta

class AssetLifecycleManager:
    """Manage asset lifecycle and cleanup."""

    def __init__(self, store: AssetStore, db, archive_storage):
        self.store = store
        self.db = db
        self.archive = archive_storage

    def apply_retention_policy(self, policy: dict):
        """Apply retention policy to assets."""

        now = datetime.utcnow()

        # Find assets matching policy criteria
        if policy["type"] == "age":
            cutoff = now - timedelta(days=policy["days"])
            assets = self.db.query(
                "assets",
                {"created_at": {"$lt": cutoff.isoformat()}}
            )
        elif policy["type"] == "unused":
            cutoff = now - timedelta(days=policy["days"])
            assets = self.db.query(
                "assets",
                {"usage.last_accessed": {"$lt": cutoff.isoformat()}}
            )

        for asset in assets:
            if policy["action"] == "archive":
                self._archive_asset(asset["id"])
            elif policy["action"] == "delete":
                self._delete_asset(asset["id"])

    def _archive_asset(self, asset_id: str):
        """Move asset to archive storage."""

        content, metadata = self.store.get(asset_id)

        # Upload to archive
        self.archive.upload(content, f"archive/{asset_id}")

        # Update status
        self.db.update("assets", asset_id, {"status": "archived"})

        # Remove from primary storage
        self.store.delete(asset_id)

    def _delete_asset(self, asset_id: str):
        """Permanently delete asset."""

        # Soft delete first
        self.db.update("assets", asset_id, {
            "status": "deleted",
            "deleted_at": datetime.utcnow().isoformat()
        })

        # Hard delete after grace period
        # (Would be scheduled for later)

    def restore_from_archive(self, asset_id: str):
        """Restore archived asset."""

        content = self.archive.download(f"archive/{asset_id}")
        metadata = self.db.get("assets", asset_id)

        self.store.store(content, metadata)
        self.db.update("assets", asset_id, {"status": "active"})
```

### Pattern 5: Usage Tracking

```python
class AssetUsageTracker:
    """Track asset usage for analytics and billing."""

    def __init__(self, db):
        self.db = db

    def record_usage(
        self,
        asset_id: str,
        action: str,
        user_id: str,
        context: dict = None
    ):
        """Record asset usage event."""

        event = {
            "asset_id": asset_id,
            "action": action,  # "view", "download", "embed", "transform"
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        }

        self.db.insert("asset_usage", event)

        # Update asset usage stats
        self.db.update(
            "assets",
            asset_id,
            {
                "$inc": {f"usage.{action}_count": 1},
                "$set": {"usage.last_accessed": event["timestamp"]}
            }
        )

    def get_usage_report(self, time_range: str = "30d") -> dict:
        """Generate usage report."""

        return self.db.aggregate("asset_usage", [
            {"$match": {"timestamp": {"$gte": self._get_start_date(time_range)}}},
            {"$group": {
                "_id": "$action",
                "count": {"$sum": 1},
                "unique_assets": {"$addToSet": "$asset_id"},
                "unique_users": {"$addToSet": "$user_id"}
            }}
        ])

    def get_popular_assets(self, limit: int = 10) -> list:
        """Get most used assets."""

        return self.db.query(
            "assets",
            {"status": "active"},
            sort={"usage.download_count": -1},
            limit=limit
        )
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No deduplication | Wasted storage | Content-addressable storage |
| Missing metadata | Can't search/organize | Rich metadata schema |
| No versioning | Can't revert changes | Version control |
| Local-only storage | Single point of failure | Cloud backup |
| No lifecycle policy | Storage grows forever | Retention policies |

## Tools & References

### Related Skills
- faion-image-gen-skill
- faion-video-gen-skill
- faion-audio-skill

### Related Agents
- faion-multimodal-agent

### External Resources
- [MinIO](https://min.io/) - S3-compatible storage
- [Elasticsearch](https://www.elastic.co/) - Search/indexing
- [CLIP](https://openai.com/research/clip) - Visual embeddings
- [DVC](https://dvc.org/) - Data/model versioning

## Checklist

- [ ] Designed storage architecture
- [ ] Implemented content-addressable storage
- [ ] Added cloud storage integration
- [ ] Created metadata schema
- [ ] Set up search indexing
- [ ] Added visual similarity search
- [ ] Implemented versioning
- [ ] Created collections/organization
- [ ] Set up lifecycle policies
- [ ] Added usage tracking

---

*Methodology: M-GEN-008 | Category: Multimodal/Generation*
*Related: faion-multimodal-agent*
