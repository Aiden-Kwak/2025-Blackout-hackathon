import React from 'react';

function URLManagement() {
    const devBaseURL = `http://localhost:8000`; // 개발 환경
    const prodBaseURL = `http://54.152.161.95:3000`; // 프로덕션 환경

    return process.env.NODE_ENV === 'development' ? devBaseURL : prodBaseURL;
}

export default URLManagement;