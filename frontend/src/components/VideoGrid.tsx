import { useState } from 'react'
import Image from 'next/image'

interface Video {
  id: string
  title: string
  thumbnail: string
  channelTitle: string
  explanation: string
}

export function VideoGrid() {
  const [videos, setVideos] = useState<Video[]>([])

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold text-gray-900">Recommended Videos</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {videos.length > 0 ? (
          videos.map((video) => (
            <div key={video.id} className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="aspect-video relative">
                <Image
                  src={video.thumbnail}
                  alt={video.title}
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-4">
                <h3 className="font-medium text-gray-900 line-clamp-2">{video.title}</h3>
                <p className="text-sm text-gray-500 mt-1">{video.channelTitle}</p>
                <p className="text-sm text-gray-700 mt-2 line-clamp-2">{video.explanation}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-12 bg-white rounded-lg">
            <p className="text-gray-500">Start a conversation to get video recommendations</p>
          </div>
        )}
      </div>
    </div>
  )
} 