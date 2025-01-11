const getBaseURL = () => {
  const baseURLs = {
    development: `http://localhost:8000`, // 개발 환경
    production: `http://aiden-kwak.com`, // 프로덕션 환경
  };

  // NODE_ENV 값에 따라 URL 반환, 기본값은 개발 환경
  return baseURLs[process.env.NODE_ENV] || baseURLs.development;
};

const url = getBaseURL();

/** @type {import('next').NextConfig} */
const nextConfig = {

    async rewrites() {
      return [
        {
          source: "/api/:path*/",
          destination: `${url}/api/:path*/`,
        },
        {
          source: "/media/:path*/",
          destination: `${url}/media/:path*/`,
        },
      ];
    },
    trailingSlash: true,
  };
  
  export default nextConfig;