const button = document.querySelector('button');
const addToCart = document.querySelector('.add-to-cart');
const addedToCart = document.querySelector('.added-to-cart');
const cart = document.querySelector('.fa-shopping-cart');
const bag = document.querySelector('.fa-shopping-bag');

button.addEventListener('click', () => {
    addToCart.classList.add('add-to-cart-animation')
    addedToCart.classList.add('added-to-cart-animation')

    cart.style.animation = 'cart 2000ms ease-in-out forwards'
    bag.style.animation = 'bag 2000ms 700ms ease-in-out forwards'
})