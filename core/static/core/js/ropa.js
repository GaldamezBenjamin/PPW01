fetch("http://fakestoreapi.com/products")
.then((response) => response.json())
.then((data) => {
  const container = document.getElementById("container");
  data.forEach((product) => {
    const productCard = document.createElement("div");
    productCard.classList.add("col", "p-2", "d-flex");
    const truncatedDescription =
      product.description.substring(0, 200) +
      (product.description.length > 200 ? "..." : "");

      productCard.innerHTML = `
      <div class="col">
        <div class="card mb-4 box-shadow">
          <div class="card pt-2 flex-column text-center" style="height: 500px">
            <img src="${product.image}" style="height: 350px; max-width: 100%; object-fit: contain;" class="caratulas"/>
          </div>
          <div class="card-body">
            <h5 class="card-title">${product.title}</h5>
              <div class="card-text">
                <div class="lead text-terciary">${truncatedDescription}</div>
                <br/>
              </div>
              <div class="card-footer">
                <div class="lead">
                  <span class="sale-real-price fw-bold">$${product.price}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    container.appendChild(productCard);
  });
});