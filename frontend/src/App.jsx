import { useAuth } from './hooks/useAuth';
import Auth from './components/Auth';
import Dashboard from './components/Dashboard';
import './App.css';

export default function App() {
  const { user, loading, logout } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app">
      {user ? (
        <Dashboard onLogout={logout} />
      ) : (
        <Auth onAuthSuccess={() => window.location.reload()} />
      )}
    </div>
  );
}
