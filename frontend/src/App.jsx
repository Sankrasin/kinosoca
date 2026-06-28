import { Outlet } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";

function App() {
  return (
    <AuthProvider>
      <div className="flex flex-col min-h-screen bg-gray-900">
        <Navbar />
        <main className="flex-1 container mx-auto px-4 py-8 pt-24">
          <Outlet />
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
}

export default App;
