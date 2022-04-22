import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import registerServiceWorker from './registerServiceWorker';
import { BrowserRouter, Route, Routes, Link } from "react-router-dom";

import Search from "./routes/search";
import Setting from "./routes/setting";
import Register from "./routes/register";
import Login from "./routes/login";
import CreatePage from "./routes/create-page";

ReactDOM.render(
    <div>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Search />} />
                <Route path="search" element={<Search />} />
                <Route path="setting" element={<Setting />} />
                <Route path="register" element={<Register />} />
                <Route path="login" element={<Login />} />
                <Route path="create-page" element={<CreatePage />} />
            </Routes>
        </BrowserRouter>
    </div>, document.getElementById('root'));
registerServiceWorker();
