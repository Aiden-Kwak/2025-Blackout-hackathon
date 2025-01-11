import Image from "next/image";
import styles from "./page.module.css";
import LoginButton from "@/components/loginButton";

export default function Home() {
  return (
    <div>
      <main>
        <h1>ExactLLM</h1>
        <ol>
          <li>
            Upload PDF.
          </li>
          <li>Chat with your PDF and get exact information.</li>
        </ol>

        <div>
          <LoginButton />
          <a
            href="https://github.com/Aiden-Kwak"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.secondary}
          >
            My Github
          </a>
        </div>
      </main>
    </div>
  );
}