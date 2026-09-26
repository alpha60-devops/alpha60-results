"use strict";
document.querySelectorAll(".h15-slice").forEach(section => {
  const search = section.querySelector(".slice-search");
  const basis = section.querySelector(".slice-basis");
  const thresholdEnabled = section.querySelector(".slice-threshold-enabled");
  const threshold = section.querySelector(".slice-threshold");
  const production = section.querySelector(".slice-production");
  const citizensEnabled = section.querySelector(".slice-citizens-enabled");
  const citizens = section.querySelector(".slice-citizens");
  const rows = [...section.querySelectorAll("tbody tr")].map(row => ({
    row,
    actors: Number(row.cells[1].textContent.trim()),
    creators: Number(row.cells[2].textContent.trim()),
    usaProduction: row.cells[3].textContent.trim() === "true",
    usaCitizens: Number(row.cells[4].textContent.trim()),
  }));
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    const minimumPeople = Number(threshold.value);
    const minimumCitizens = Number(citizens.value);
    let visible = 0;
    rows.forEach(({row, actors, creators, usaProduction, usaCitizens}) => {
      row.hidden = Boolean(
        (query && !row.textContent.toLocaleLowerCase().includes(query)) ||
        (basis.value && !row.dataset.basis.split(" ").includes(basis.value)) ||
        (thresholdEnabled.checked && actors + creators < minimumPeople) ||
        (production.checked && !usaProduction) ||
        (citizensEnabled.checked && usaCitizens < minimumCitizens)
      );
      visible += !row.hidden;
    });
    section.querySelector(".slice-visible").textContent = `${visible} of ${rows.length} candidate rows shown. Country graphics use the full confirmed slice.`;
  };
  [search, basis, thresholdEnabled, threshold, production, citizensEnabled, citizens]
    .forEach(input => input.addEventListener("input", update));
  threshold.addEventListener("change", () => {
    thresholdEnabled.checked = true;
    update();
  });
  citizens.addEventListener("change", () => {
    citizensEnabled.checked = true;
    update();
  });
  update();
});
