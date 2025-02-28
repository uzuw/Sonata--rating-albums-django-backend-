import { Link } from 'react-router-dom';
import { FaHome, FaUser } from 'react-icons/fa';
import { BsFillMusicPlayerFill } from 'react-icons/bs';
import { IoLibrarySharp } from 'react-icons/io5';

const Sidebar = () => {
  return (

    <div className="fixed mt-20 left-5 h-1/2 w-16 bg-white border-2 opacity-75 flex flex-col items-center justify-between py-4 rounded-3xl gap-6 shadow-lg">
      <Link to="/" className="hover:scale-110 transition-all transform duration-200 z-10">
        <FaHome className="text-black text-3xl inline-block" />
      </Link>
      <Link to="/tracks" className="hover:scale-110 transition-all transform duration-100">
        <BsFillMusicPlayerFill className="text-black text-3xl inline-block" />
      </Link>
      <Link to="/library" className="hover:scale-110 transition-all transform duration-100">
        <IoLibrarySharp className="text-black text-3xl inline-block" />
      </Link>
      <Link to="/profile" className="hover:scale-110 transition-all transform duration-100">
        <FaUser className="text-black text-3xl inline-block" />
      </Link>
    </div>

    
  );
};

export default Sidebar;