import Image from 'next/image';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar */}
      <header className="flex justify-between items-center bg-emerald-400 px-6 py-4 ">
        <div className="text-lg font-bold text-lime-50">Reviewrise.ai</div>
        <div className="space-x-4">
          <Link href="/signup"className="px-4 py-2 text-xs font-medium text-lime-50 border border-lime-50 rounded-lg hover:bg-lime-50 hover:text-black ">
            Signup
          </Link>
          <Link href="/login" className="px-4 py-2 text-xs font-medium text-lime-50 bg-emerald-900 rounded-lg hover:bg-gray-800">
            Login
          </Link>
          <Link
            href="/dashboard"
            className="px-4 py-2 text-xs font-medium text-lime-50 bg-emerald-900 rounded-lg hover:bg-gray-800"
          >
            Dashboard
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex flex-col items-center justify-center flex-1 bg-emerald-400 text-center px-4">
        <h1 className="text-4xl font-extrabold mb-4 text-lime-50 mt-10" >Reviewrise.ai</h1>
        <p className="text-lg font-bold  text-lime-50 mb-6">
          Collect all your reviews into a comprehensive analysis
        </p>
        <Link href="/signup" className="px-4 py-3 text-sm text-white bg-emerald-900 rounded-lg hover:bg-gray-800">
          Create Analysis
        </Link>

        <div className="mt-10">
          <Image 
          src="/homepage-image.png"
          alt="Hero image"
          width={500}
          height={400}
          className="rounded-lg"
          />

        </div>
      </main>

      {/* Footer */}
      <footer className="text-lime-50 bg-emerald-400 py-10 ">
        <div className="container mx-auto px-6 pr-11">
          <div className="flex justify-between items-center">
            <div className="text-sm font-medium">© 2024 Reviewrise.ai</div>
            <div className="space-x-4">
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
