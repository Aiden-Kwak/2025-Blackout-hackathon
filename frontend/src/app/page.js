import Image from "next/image";
import styles from "./page.module.css";
import LoginButton from "@/components/loginButton";
import { redirect } from 'next/navigation';

export default function Home() {
  redirect('/main');
  //<LoginButton />
  return null;
}