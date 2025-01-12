"use client";

import { useState } from "react";
import AuthStatus from "@/utils/authStatus";
import Image from "next/image";
import styles from "@/app/page.module.css";
import URLManagement from "@/utils/URLManagement";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock, faLockOpen } from '@fortawesome/free-solid-svg-icons';
import "./loginButton.css";

function LoginButton() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const url = URLManagement();

  console.log(url);

  return (
    <>
      {/* AuthStatus가 상태를 업데이트 */}
      <AuthStatus onStatusChange={setIsLoggedIn} />
      <a
        className={styles.primary}
        href={
          isLoggedIn
            ? "/main" // 로그인 상태일 때
            : `${url}/api/accountapp/auth/login/?next=${url}/main` // 비로그인 상태일 때
        }
        target={isLoggedIn ? "_self" : "_blank"}
        rel="noopener noreferrer"
      >
        <FontAwesomeIcon 
            icon={isLoggedIn ? faLockOpen : faLock} 
            size="1x"
            color={isLoggedIn ? "white" : "white"}
            className={`lock-icon ${isLoggedIn ? "unlocked" : "locked"}`} 
        />
      </a>
    </>
  );
}

export default LoginButton;