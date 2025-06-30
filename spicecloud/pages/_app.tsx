import '../styles/globals.css'
import type { AppProps } from 'next/app'
import Head from 'next/head'
import React from 'react'

export default function App({ Component, pageProps }: AppProps) {
  return (
      <>
        <Head>
          <title>SpiceCloud | Powered by SpiceCodeCLI</title>
        </Head>
      
        <Component {...pageProps} />
      </>
  )
  
}