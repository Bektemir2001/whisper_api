<?php

namespace App\Console\Commands;

use App\Mail\SendMessageMail;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Mail;

class SendMessageCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'send-message';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Send message to users';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $users = DB::table('users')->get();
        foreach ($users as $user)
        {
            Mail::to($user->email)->send(new SendMessageMail($user));
            print_r("send message successfully to ".$user->email."\n");
        }
    }
}
