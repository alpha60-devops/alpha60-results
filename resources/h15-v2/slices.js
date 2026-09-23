"use strict";
document.querySelectorAll(".h15-slice").forEach(section => {
  const search = section.querySelector(".slice-search");
  const basis = section.querySelector(".slice-basis");
  const us = section.querySelector(".slice-us");
  const rows = [...section.querySelectorAll("tbody tr")];
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    rows.forEach(row => {
      row.hidden = (query && !row.textContent.toLocaleLowerCase().includes(query)) ||
        (basis.value && !row.dataset.basis.split(" ").includes(basis.value)) ||
        (us.checked && row.dataset.us !== "true");
      visible += !row.hidden;
    });
    section.querySelector(".slice-visible").textContent = `${visible} of ${rows.length} candidate rows shown. Country graphics use the full confirmed slice.`;
  };
  [search, basis, us].forEach(input => input.addEventListener("input", update));
  update();
});
