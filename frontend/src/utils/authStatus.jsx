"use client";

import { useState, useEffect } from "react";
import apiClient from "@/utils/axios";

function AuthStatus({ onStatusChange }) {
  const [isLoggedIn, setIsLoggedIn] = useState(null);

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await apiClient.get("/api/accountapp/me/");
        const loggedIn = response.status === 200;
        setIsLoggedIn(loggedIn);
        onStatusChange(loggedIn);
      } catch (error) {
        setIsLoggedIn(false);
        onStatusChange(false);
      }
    };

    checkLoginStatus();
  }, [onStatusChange]);

  if (isLoggedIn === null) {
    return <div>Loading...</div>;
  }

  return null; // 상태만 업데이트하고 렌더링은 하지 않음
}

export default AuthStatus;