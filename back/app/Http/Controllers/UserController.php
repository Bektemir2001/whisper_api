<?php

namespace App\Http\Controllers;

use App\Http\Requests\RegisterRequest;
use Carbon\Carbon;
use Exception;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Illuminate\View\View;

class UserController extends Controller
{
    public function index(): View
    {
        $users = DB::table('users')->orderBy('id', 'desc')->get();
        return view('user.register' , compact('users'));
    }

    public function register(RegisterRequest $request): RedirectResponse
    {

        try{
            $data = $request->validated();
            $data['token'] = $this->generateToken();
            $data['has_access'] = true;
            $data['limit'] = 30;
            DB::table('users')->insert($data);
            return redirect()->route('home')->with(['notification' => 'done']);
        }
        catch (Exception $exception)
        {
            return redirect()->route('index')->with(['notification' => $exception->getMessage()]);
        }
    }

    public function generateToken(): string
    {
        $randomString = Str::random(150);
        $salt1 = Carbon::now();
        $salt2 = Str::random(50);

        $part1 = hash('sha256', $salt1 . $randomString);
        $part2 = hash('sha256', $salt2 . $randomString);

        return $part1 . $part2;
    }
}
