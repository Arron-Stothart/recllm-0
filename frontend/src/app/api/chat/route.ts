import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { message } = body

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://10.20.26.107:7860'
    
    const apiEndpoint = `${API_URL}/api/chat?__token=${process.env.HUGGING_FACE_HUB_TOKEN}`
    console.log('Attempting to fetch from:', apiEndpoint)

    const response = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.HUGGING_FACE_HUB_TOKEN}`
      },
      body: JSON.stringify({
        user_id: 'default_user',
        messages: [{ role: 'user', content: message }]
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Backend response error:', errorText)
      throw new Error(`Failed to fetch response from backend: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error in chat API route:', error)
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 }
    )
  }
} 