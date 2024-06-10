import React, { useEffect, useState } from 'react';
import api from './api'; // Import the Axios instance we created
import axios from 'axios';
function ArticleList() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await api.get('/article/');
        setArticles(response.data);
      } catch (error) {
        console.error("Error fetching articles:", error);
      }
    }

    fetchData();
  }, []);

  return (
    <div>
      {articles.map((article, index) => (
        <div key={index}>
          {/* Display article properties */}
          <h2>{article.title}</h2>
          {/* Add more fields as needed */}
        </div>
      ))}
    </div>
  );
}

export default ArticleList;