/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    HUGGING_FACE_HUB_TOKEN: process.env.HUGGING_FACE_HUB_TOKEN,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL
  }
}

module.exports = nextConfig 