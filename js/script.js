// Copia los productos de index.html 20 veces
if (document.getElementById('mini_producto')) {
    var tarjeta = document.getElementById('mini_producto').outerHTML;
    var tarjetas = '';
    for (i = 0; i < 20; i++) {
        tarjetas = tarjetas + tarjeta;
    }
    document.getElementById('mini_producto').outerHTML = tarjetas;
}

// Lee el contenido de un archivo llamado "menu_superior.html" donde está el código del menú de las páginas y lo copia al inicio de cada página
if (document.getElementById('menu')) {
    fetch('menu_superior.html').then(response => {
        return response.text();
    }).then(htmlContent => {
        document.getElementById('menu').innerHTML = htmlContent;
        window.scrollTo(0, 0);
    });
};


// es del login // 
document.querySelector('form').addEventListener('submit', function(event) {
    var username = document.querySelector('input[type="text"]').value;
    var password = document.querySelector('input[type="password"]').value;
  
    if (username === '' || password === '') {
      event.preventDefault(); // Evita el envío del formulario si los campos están vacíos
      alert('Por favor, completa todos los campos.');
    }
  });



  // codigo de las fichas de productos creando una lista para manejar ids y precios
  const products = [
    {
      id: 1,
      image: "img/diablo4.webp",
      name: "Diablo IV",
      description: "Juego de acción y rol desarrollado por Blizzard Entertainment.",
      realPrice: 69990,
      offerPrice: 34990
    },
    {
      id: 2,
      image: "img/re4remake.webp",
      name: "Resident Evil 4 (REMAKE)",
      description: "Juego de acción y aventura desarrollado por Capcom.",
      realPrice: 49990,
      offerPrice: 24990
    },
    {
      id: 3,
      image: "img/dmc5.webp",
      name: "Devil May Cry 5",
      description: "Juego de acción y aventura desarrollado por Capcom.",
      realPrice: 19990,
      offerPrice: 9990
    },
    {
      id: 4,
      image: "img/godofwar.jpg",
      name: "God of war (2018)",
      description: "Juego de acción y aventura desarrollado por Sony Interactive Entertainment.",
      realPrice: 29990,
      offerPrice: 14990
    },
    {
      id: 5,
      image: "img/gowragnarok.webp",
      name: "God of War RAGNAROK",
      description: "Juego de acción y aventura desarrollado por Sony Interactive Entertainment.",
      realPrice: 59990,
      offerPrice: 29990
    },
    {
      id: 6,
      image: "img/gta5.jpg",
      name: "Grand Theft Auto 5",
      description: "Juego de acción y aventura desarrollado por Rockstar Games.",
      realPrice: 13990,
      offerPrice: 6990
    }
  ];


  // Función para mostrar la información del producto
function showProductDetails(productId) {
  const productEl = document.querySelector(`[data-product-id="${productId}"]`);
  const product = products.find((p) => p.id == productId);

  // Aquí puedes actualizar los elementos del DOM con la información del producto
  productEl.querySelector(".card-title").textContent = product.name;
  productEl.querySelector(".sale-real-price").textContent = `$${product.realPrice}`;
  productEl.querySelector(".sale-offer-price").textContent = `$${product.offerPrice}`;
  productEl.querySelector(".product-image-link img").src = product.image;

}

document.querySelectorAll(".product-image-link").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault(); // Evita que el enlace cargue una nueva página
    const productId = event.currentTarget.closest("[data-product-id]").dataset.productId;
    showProductDetails(productId);
  });
});



///

// Función para mostrar el menú de cliente
function showClientMenu() {
  const navMenu = document.getElementById('nav-menu');
  navMenu.innerHTML = `
      <li class="nav-item">
          <a class="nav-link inicio" aria-current="page" href="index.html">Inicio</a>
      </li>
      <li class="nav-item">
          <a class="nav-link nosotros" href="nosotros.html">Nosotros</a>
      </li>
      <li class="nav-item">
          <a class="nav-link mis-datos" href="#">Mis datos</a>
      </li>
      <li class="nav-item">
          <a class="nav-link mis-compras" href="#">Mis compras anteriores</a>
      </li>
      <li class="nav-item">
          <a class="nav-link cerrar-sesion" href="#" onclick="logoutUser()">Cerrar sesión</a>
      </li>
  `;
}

// Función para mostrar el menú de admin
function showAdminMenu() {
  const navMenu = document.getElementById('nav-menu');
  navMenu.innerHTML = `
      <li class="nav-item">
          <a class="nav-link inicio" aria-current="page" href="index.html">Inicio</a>
      </li>
      <li class="nav-item">
          <a class="nav-link nosotros" href="nosotros.html">Nosotros</a>
      </li>
      <li class="nav-item">
          <a class="nav-link admin-panel" href="#">Panel de Admin</a>
      </li>
      <li class="nav-item">
          <a class="nav-link cerrar-sesion" href="#" onclick="logoutUser()">Cerrar sesión</a>
      </li>
  `;
}

// Función para cerrar sesión y restablecer el menú
function logoutUser() {
  // Aquí puedes agregar lógica para cerrar sesión, como eliminar tokens o cookies
  showInitialMenu();
}

// Función para mostrar el menú inicial
function showInitialMenu() {
  const navMenu = document.getElementById('nav-menu');
  navMenu.innerHTML = `
      <li class="nav-item">
          <a class="nav-link inicio" aria-current="page" href="index.html">Inicio</a>
      </li>
      <li class="nav-item">
          <a class="nav-link nosotros" href="nosotros.html">Nosotros</a>
      </li>
      <li class="nav-item">
          <a class="nav-link ingreso" href="ingreso.html">Ingresar</a>
      </li>
  `;
}




function logout() {
  // Obtener el elemento del menú de navegación
  const navMenu = document.getElementById('nav-menu');

  // Restablecer el contenido del menú de navegación
  navMenu.innerHTML = `
      <li class="nav-item">
          <a class="nav-link inicio" aria-current="page" href="index.html">Inicio</a>
      </li>
      <li class="nav-item">
          <a class="nav-link nosotros" href="nosotros.html">Nosotros</a>
      </li>
      <li class="nav-item">
          <a class="nav-link ingreso" href="ingreso.html">Ingresar</a>
      </li>
  `;

     // Eliminar cualquier clase activa del menú
     const navLinks = navMenu.getElementsByTagName('a');
     for (let i = 0; i < navLinks.length; i++) {
         navLinks[i].classList.remove('active');
     }
 
     // Agregar la clase activa al enlace de "Inicio"
     const homeLink = navMenu.querySelector('.inicio');
     homeLink.classList.add('active');
 }



// Variables para almacenar el estado de inicio de sesión y el tipo de usuario
let isLoggedIn = false;
let userType = null; // 'client' o 'admin'

// Función para mostrar el menú de cliente
function showClientMenu() {
    isLoggedIn = true;
    userType = 'client';
    updateNavMenu();
}

// Función para mostrar el menú de admin
function showAdminMenu() {
    isLoggedIn = true;
    userType = 'admin';
    updateNavMenu();
}

// Función para cerrar sesión
function logout() {
    isLoggedIn = false;
    userType = null;
    updateNavMenu();
}

// Función para actualizar el menú de navegación
function updateNavMenu() {
    const navMenu = document.getElementById('nav-menu');
    navMenu.innerHTML = '';

    // Agregar elementos al menú según el tipo de usuario
    const menuItems = [
        { label: 'Inicio', href: 'index.html', visible: true },
        { label: 'Nosotros', href: 'nosotros.html', visible: true },
        { label: 'Mis datos', href: 'misdatos.html', visible: isLoggedIn },
        { label: 'Mis compras', href: '#', visible: isLoggedIn && userType === 'client' },
        { label: 'Panel de Admin', href: '#', visible: isLoggedIn && userType === 'admin' },
        { label: 'Cerrar sesión', href: '#', visible: isLoggedIn, onClick: logout }
    ];

    menuItems.forEach(item => {
        if (item.visible) {
            const li = document.createElement('li');
            li.classList.add('nav-item');
            const a = document.createElement('a');
            a.classList.add('nav-link');
            a.textContent = item.label;
            a.href = item.href;
            if (item.onClick) {
                a.addEventListener('click', item.onClick);
            }
            li.appendChild(a);
            navMenu.appendChild(li);
        }
    });
}

// que
if (document.getElementById('footer')) {
    fetch('footer.html').then(response => {
        return response.text();
    }).then(htmlContent => {
        document.getElementById('footer').innerHTML = htmlContent;
        window.scrollTo(0, 0);
    });
};