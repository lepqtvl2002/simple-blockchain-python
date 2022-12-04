const showMoreBtns = document.querySelectorAll(".btn-show-more");

showMoreBtns.forEach((btnShowMore) => {
  btnShowMore.onclick = () => {
    const postContent = btnShowMore.parentElement;
    postContent.querySelector(".content-more").classList.toggle("d-none");
    const icon = btnShowMore.querySelector("i");
    icon.classList.toggle("bi-chevron-compact-up");
  };
});
