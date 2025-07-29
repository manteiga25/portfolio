var rating = document.getElementsByClassName("collapse-btn");

  // Itera sobre cada botão
  for (let i = 0; i < rating.length; i++) {
    rating[i].addEventListener("click", function() {
      // Alterna a classe 'active' no botão
      this.classList.toggle("active");

      // Obtém o ID do conteúdo alvo do atributo data-target
      var targetId = this.getAttribute("data-target");
      // Encontra o elemento de conteúdo correspondente
      var content = document.getElementById(targetId);

      // Verifica se o elemento de conteúdo foi encontrado
      if (!content) {
        console.error("Collapse content with ID '" + targetId + "' not found.");
        return; // Sai da função se o conteúdo não for encontrado
      }

      // Expande ou retrai o conteúdo alterando o maxHeight
      if (content.style.maxHeight && content.style.maxHeight !== "0px") {
        // Se estiver expandido, recolhe
        content.style.maxHeight = "0px";
        // Opcional: Remover a classe 'active' do conteúdo se estiver usando-a
        // content.classList.remove("active");
      } else {
        // Se estiver recolhido, expande
        content.style.maxHeight = content.scrollHeight + "px";
        // Opcional: Adicionar a classe 'active' ao conteúdo se estiver usando-a
        // content.classList.add("active");
      }
    });
  }

  var courses = document.getElementsByClassName("collapse-btn-courses");

  // Itera sobre cada botão
  for (let i = 0; i < courses.length; i++) {
    courses[i].addEventListener("click", function() {
      // Alterna a classe 'active' no botão
      this.classList.toggle("active");

      // Obtém o ID do conteúdo alvo do atributo data-target
      var targetId = this.getAttribute("data-book-target");
      // Encontra o elemento de conteúdo correspondente
      var content = document.getElementById(targetId);

      // Verifica se o elemento de conteúdo foi encontrado
      if (!content) {
        console.error("Collapse content with ID '" + targetId + "' not found.");
        return; // Sai da função se o conteúdo não for encontrado
      }

      // Expande ou retrai o conteúdo alterando o maxHeight
      if (content.style.maxHeight && content.style.maxHeight !== "0px") {
        // Se estiver expandido, recolhe
        content.style.maxHeight = "0px";
        // Opcional: Remover a classe 'active' do conteúdo se estiver usando-a
        // content.classList.remove("active");
      } else {
        // Se estiver recolhido, expande
        content.style.maxHeight = content.scrollHeight + "px";
        // Opcional: Adicionar a classe 'active' ao conteúdo se estiver usando-a
        // content.classList.add("active");
      }
    });
  }