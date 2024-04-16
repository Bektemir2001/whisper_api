<?php

use App\Http\Controllers\UserController;
use Illuminate\Support\Facades\Route;

Route::get('/', [UserController::class, 'index'])->name('home');
Route::post('/', [UserController::class, 'register'])->name('register');
Route::get('/send/{user}', [UserController::class, 'sendMail'])->name('sendMail');
