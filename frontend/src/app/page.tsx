"use client"

import { VideoGrid } from '@/components/VideoGrid'
import { ChatInterface } from '@/components/ChatInterface'
import { UserProfile } from '@/components/UserProfile'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">RecLLM</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left sidebar - User Profile */}
          <div className="lg:col-span-1">
            <UserProfile />
          </div>
          
          {/* Main content - Video Grid */}
          <div className="lg:col-span-2">
            <VideoGrid />
          </div>
        </div>
        
        {/* Chat Interface - Fixed at bottom */}
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t">
          <div className="container mx-auto px-4">
            <ChatInterface />
          </div>
        </div>
      </div>
    </main>
  )
}
