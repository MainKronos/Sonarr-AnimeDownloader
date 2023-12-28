import type { ReactNode } from 'react';

import './style.scss';

interface ModalProps{
    activationState: [boolean, (state:boolean)=> void]
    children?: ReactNode
}

export function Modal({activationState, children}:ModalProps){
    const [state, setState] = activationState;

    document.body.style.overflow = state ? 'hidden' : 'auto';

    if(state){
        return (
            <div className='modal'>
                <div onClick={()=>setState(false)}></div>
                <section>
                    {children}
                </section>
            </div>
        )
    }
}