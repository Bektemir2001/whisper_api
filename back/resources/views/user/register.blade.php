<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://demos.creative-tim.com/notus-js/assets/styles/tailwind.css">
    <link rel="stylesheet" href="https://demos.creative-tim.com/notus-js/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css">

    <title>ASR Registration</title>
</head>
<body>
<div class="bg-white border rounded-lg px-8 py-6 mx-auto my-8 max-w-2xl">
    <h2 class="text-2xl font-medium mb-4">Каттоо</h2>
    <form action="{{route('register')}}" method="POST">
        @csrf
        <div class="mb-4">
            <label for="name" class="block text-gray-700 font-medium mb-2">Команданын аталышы</label>
            <input type="text" id="name" name="name" value="{{old('name')}}"
                   class="border border-gray-400 p-2 w-full rounded-lg focus:outline-none focus:border-blue-400" required>
            @error('name')
                <p class="text-red-500">{{$message}}</p>
            @enderror
        </div>
        <div class="mb-4">
            <label for="email" class="block text-gray-700 font-medium mb-2">Почта</label>
            <input type="email" id="email" name="email" value="{{old('email')}}"
                   class="border border-gray-400 p-2 w-full rounded-lg focus:outline-none focus:border-blue-400" required>
            @error('email')
            <p class="text-red-500">{{$message}}</p>
            @enderror
        </div>
        <div class="mb-4">
            <label for="device" class="block text-gray-700 font-medium mb-2">GPU</label>
            <select id="device" name="device"
                    class="border border-gray-400 p-2 w-full rounded-lg focus:outline-none focus:border-blue-400" required>
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
            </select>
        </div>
        <div>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Каттоо</button>
        </div>
    </form>
</div>


<!-- component -->


<section class="py-1 bg-blueGray-50">
    <div class="w-full xl:w-10/12 mb-12 xl:mb-0 px-4 mx-auto mt-24">
        <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded ">
            <div class="rounded-t mb-0 px-4 py-3 border-0">
                <div class="flex flex-wrap items-center">
                    <div class="relative w-full px-4 max-w-full flex-grow flex-1">
                        <h3 class="font-semibold text-base text-blueGray-700">Командалар</h3>
                    </div>

                </div>
            </div>

            <div class="block w-full overflow-x-auto">
                <table class="items-center bg-transparent w-full border-collapse ">
                    <thead>
                    <tr>
                        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                            Команданын аталышы
                        </th>
                        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                            Почта
                        </th>
                        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                            Токен
                        </th>
                        <th class="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                            device
                        </th>

                    </tr>
                    </thead>

                    <tbody>
                    @foreach($users as $user)
                        <tr>
                            <th class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left text-blueGray-700 ">
                                {{$user->name}}
                            </th>
                            <th class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left text-blueGray-700 ">
                                {{$user->email}}
                            </th>
                            <td class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 ">
                                {{$user->token}}
                            </td>
                            <td class="border-t-0 px-6 align-center border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                                {{$user->device}}
                            </td>
                        </tr>
                    @endforeach


                    </tbody>

                </table>
            </div>
        </div>
    </div>
</section>
</body>
</html>
