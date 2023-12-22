import './style.scss';

class ContextMenu {
    menu: HTMLUListElement;

    constructor(){
        const menu = document.createElement('ul');
        this.menu = menu;
        menu.id = 'menu';
        document.body.prepend(menu);

        document.addEventListener('click', this.hide);
    }

    hide = (event:Event) => {
        this.menu.classList.remove('active');
        while(this.menu.firstChild) this.menu.removeChild(this.menu.firstChild);
    }

    show = (event:MouseEvent, callbacks:{[label:string]: EventListener}) => {
        event.preventDefault();

        if(this.menu.classList.contains('active')) this.hide(event);

        Object.entries(callbacks).map(([label, callback]) => {
            const li = document.createElement('li');
            li.textContent = label;
            li.addEventListener('click', callback);
            this.menu.appendChild(li);
        });

        this.menu.style.top = `${event.pageY}px`;
		this.menu.style.left = `${event.pageX}px`;
        this.menu.classList.add('active');
    }
}

export const Menu = new ContextMenu();