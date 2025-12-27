import React, { useState } from 'react';
import Layout from '@theme/Layout';
import ChatInterface from '../../components/ChatInterface';

export default function ChatPage() {
  return (
    <Layout title="RAG Chat" description="Chat with the RAG system">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <h1>Chat with our RAG System</h1>
            <ChatInterface />
          </div>
        </div>
      </div>
    </Layout>
  );
}