package main

import (
	"context"
	"fmt"
	"log"

	"github.com/YuanLearned/micro-svc/ai/go-client/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	// 连接到 gRPC 服务器
	conn, err := grpc.NewClient("localhost:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("failed to connect: %v", err)
	}
	defer conn.Close()

	// 创建客户端
	client := proto.NewAIServiceClient(conn)

	// 构造请求
	req := &proto.AICallRequest{
		Prompt:      "Tell me a joke about programming",
		Model:       "gpt-3.5-turbo",
		MaxTokens:   150,
		Temperature: 0.7,
	}

	// 调用服务
	ctx := context.Background()
	resp, err := client.CallAI(ctx, req)
	if err != nil {
		log.Fatalf("failed to call AI: %v", err)
	}

	// 打印结果
	fmt.Println("AI Response:")
	fmt.Println("Result:", resp.GetResult())
	fmt.Println("Model:", resp.GetModel())
	fmt.Println("Token Count:", resp.GetTokenCount())
}
