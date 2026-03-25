#!/usr/bin/env python3
"""
Python gRPC server for AI service
"""

import grpc
from concurrent import futures
import time

from proto import ai_service_pb2
from proto import ai_service_pb2_grpc

from openai import OpenAI

class AIServiceServicer(ai_service_pb2_grpc.AIServiceServicer):
    def __init__(self):
        # 👇 修复 2：新版 OpenAI 初始化方式
        self.client = OpenAI(
            api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxx"  # 换成你的真实 KEY
        )

    def CallAI(self, request, context):
        """处理 AI 调用请求"""
        try:
            # 👇 修复 3：新版 OpenAI SDK 调用方式
            response = self.client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "user", "content": request.prompt}
                ],
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )

            return ai_service_pb2.AICallResponse(
                result=response.choices[0].message.content,
                model=response.model,
                token_count=response.usage.total_tokens
            )

        except Exception as e:
            context.set_details(f"AI服务错误: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return ai_service_pb2.AICallResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ai_service_pb2_grpc.add_AIServiceServicer_to_server(AIServiceServicer(), server)

    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"✅ AI gRPC 服务启动成功，监听端口: {port}")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()