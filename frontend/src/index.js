import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { BrowserRouter, Route, Routes, Link } from "react-router-dom";

import Search from "./routes/search";
import Setting from "./routes/setting";
import Register from "./routes/register";

ReactDOM.render(
    <div>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="search" element={<Search />} />
                <Route path="setting" element={<Setting />} />
                <Route path="register" element={<Register />} />
            </Routes>
        </BrowserRouter>
    </div>, document.getElementById('root'));
registerServiceWorker();
