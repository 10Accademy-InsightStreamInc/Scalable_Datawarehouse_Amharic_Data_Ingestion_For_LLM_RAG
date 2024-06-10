import { useState, useEffect } from "react";
import React from 'react';
import api from "./api.js";
//import ArticleList from "./ArticleList.js"
//import { data } from "./data.js";
//import axios from "axios";
import "./App.css";
import DataList from "./search.jsx";
import Table from "./table.jsx";
// import Api_using_axios from "./Components/Api_using_axios.jsx";
function App() {
  const [search, setSearch] = useState("");
  console.log(search);
  return (
      <div className="flex flex-col">
        <DataList />
        <Table /> 
      </div>
  );
}

export default App;
