<?php
// app/Jobs/ExportUsersJob.php
// Batchable job: cancellation check, find_each equivalent, Bus::batch dispatch.

namespace App\Jobs;

use App\Models\User;
use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Bus;

class ExportUsersJob implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public readonly array $userIds,
        public readonly string $filePath
    ) {}

    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            return;
        }

        $users = User::whereIn('id', $this->userIds)->get();
        // Process chunk and append to $this->filePath...
    }
}

// Dispatch as a batch:
// $chunks = array_chunk($allUserIds, 500); // max 500 IDs per job
// $jobs = array_map(fn($chunk) => new ExportUsersJob($chunk, $path), $chunks);
//
// Bus::batch($jobs)
//     ->then(fn($batch) => ExportMailer::ready($batch->id)->deliver())
//     ->catch(fn($batch, $e) => Log::error('Export batch failed', ['id' => $batch->id]))
//     ->finally(fn($batch) => Export::markComplete($batch->id))
//     ->name('Export Users')
//     ->dispatch();
