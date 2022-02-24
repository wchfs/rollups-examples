<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CartesiController extends Controller
{
    public function advance(Request $request): JsonResponse
    {
        return response()->json([
            'message' => 'ok',
        ])->setStatusCode(Response::HTTP_ACCEPTED);
    }

    public function inspect(Request $request): JsonResponse
    {
        return response()->json([
            // TODO
        ]);
    }
}
