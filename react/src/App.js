import { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import ErrorBoundary from './ErrorBoundary';
import Header from './components/Header';
import Home from './pages/Home';
import AdPage from './pages/AdPage';
import NotFound from './pages/NotFound';
import './App.css';

function AppRoutes() {
  useEffect(() => {
    if (typeof window !== 'undefined' && typeof window.handleRoutes === 'function') {
      window.handleRoutes(["/", "/ad/:id", "*"]);
    }
  }, []);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/ad/:id" element={<AdPage />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <div data-easytag="id1-src/App.js" className="min-h-screen bg-white">
        <Header />
        <AppRoutes />
      </div>
    </ErrorBoundary>
  );
}
