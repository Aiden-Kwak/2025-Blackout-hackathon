"use client";

import apiClient from "@/utils/axios";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
``
function NavForm() {
    const [userEmail, setUserEmail] = useState("");
    const router = useRouter();

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                const response = await apiClient.get("/api/accountapp/me/");
                setUserEmail(response.data.email);
            } catch (error) {
                // 예상된 에러는 무시
                if (error.response && error.response.status === 401) {
                    // 401
                    setUserEmail("");
                } else {
                    console.error("Failed to fetch user info:", error);
                }
            }
        };

        fetchUserInfo();
    }, [router]);

    const handleLogout = async () => {
        try {
            await apiClient.post("/api/accountapp/auth/logout/");
            setUserEmail("");
            window.location.reload();
        } catch (error) {
            console.error("Logout failed:", error);
        }
    };

    return (
        <div>
            <div>
                <span>{userEmail ? userEmail : "You have to login."}</span>
                {userEmail && (
                    <button  className={styles.navButton} onClick={handleLogout}>
                        Logout
                    </button>
                )}
            </div>
        </div>
    );
}

export default NavForm;