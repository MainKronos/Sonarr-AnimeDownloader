import { ToastContainer as Container } from 'react-toastify';

import 'react-toastify/dist/ReactToastify.css';
import './style.scss';

export {toast} from 'react-toastify';

export function ToastContainer(){
    return <Container
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable={false}
        pauseOnHover={false}
        theme="dark"
    />
}

