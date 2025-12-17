// Global data storage
const calculationData = {
  az: "",
  wallMaterials: [],
  roofMaterials: [],
  buildingType: "",
  buildingParams: {},
};

// DOM elements - Steps
const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");
const step4 = document.getElementById("step4");
const step5 = document.getElementById("step5");

// DOM elements - Shelter Class
const shelterClass = document.getElementById("shelterClass");
const shelterClassDescription = document.getElementById(
  "shelterClassDescription"
);
const shelterClassCoefficient = document.getElementById(
  "shelterClassCoefficient"
);

// DOM elements - Wall Materials
const wallMaterialsTable = document
  .getElementById("wallMaterialsTable")
  .getElementsByTagName("tbody")[0];
const wallMaterialType = document.getElementById("wallMaterialType");
const wallSubmaterialType = document.getElementById("wallSubmaterialType");
const wallThickness = document.getElementById("wallThickness");
const saveWallMaterialButton = document.getElementById(
  "saveWallMaterialButton"
);

// DOM elements - Roof Materials
const roofMaterialsTable = document
  .getElementById("roofMaterialsTable")
  .getElementsByTagName("tbody")[0];
const roofMaterialType = document.getElementById("roofMaterialType");
const roofSubmaterialType = document.getElementById("roofSubmaterialType");
const roofThickness = document.getElementById("roofThickness");
const saveRoofMaterialButton = document.getElementById(
  "saveRoofMaterialButton"
);

// DOM elements - Navigation Buttons
const nextToStep2Button = document.getElementById("nextToStep2Button");
const nextToStep3Button = document.getElementById("nextToStep3Button");
const nextToStep4Button = document.getElementById("nextToStep4Button");
const calculateButton = document.getElementById("calculateButton");

const backToStep1Button = document.getElementById("backToStep1Button");
const backToStep2Button = document.getElementById("backToStep2Button");
const backToStep3Button = document.getElementById("backToStep3Button");
const backToStep4Button = document.getElementById("backToStep4Button");
const startOverButton = document.getElementById("startOverButton");

// DOM elements - Building Parameters
const buildingType = document.getElementById("buildingType");
const buildingHeight = document.getElementById("buildingHeight");
const buildingDensity = document.getElementById("buildingDensity");

// DOM elements - Results
const resultWarningWall = document.getElementById("resultWarningWall");
const resultWarningRoof = document.getElementById("resultWarningRoof");
const expectedProtectionWall = document.getElementById(
  "expectedProtectionWall"
);
const expectedProtectionRoof = document.getElementById(
  "expectedProtectionRoof"
);
const calculatedProtectionWall = document.getElementById(
  "calculatedProtectionWall"
);
const calculatedProtectionRoof = document.getElementById(
  "calculatedProtectionRoof"
);
const showCalculations = document.getElementById("showCalculations");
const calculationDetails = document.getElementById("calculationDetails");

// Get HOST URL for api requests
const baseUrl = window.location.origin;

// Initialize
function init() {
  // Wall Material Modal
  saveWallMaterialButton.addEventListener("click", addWallMaterial);

  // Roof Material Modal
  saveRoofMaterialButton.addEventListener("click", addRoofMaterial);

  // Navigation buttons
  nextToStep2Button.addEventListener("click", goToStep2);
  nextToStep3Button.addEventListener("click", goToStep3);
  nextToStep4Button.addEventListener("click", goToStep4);
  calculateButton.addEventListener("click", calculateResults);

  backToStep1Button.addEventListener("click", () => {
    step2.classList.add("hidden");
    step1.classList.remove("hidden");
  });

  backToStep2Button.addEventListener("click", () => {
    step3.classList.add("hidden");
    step2.classList.remove("hidden");
  });

  backToStep3Button.addEventListener("click", () => {
    step4.classList.add("hidden");
    step3.classList.remove("hidden");
  });

  backToStep4Button.addEventListener("click", () => {
    step5.classList.add("hidden");
    step4.classList.remove("hidden");
  });

  startOverButton.addEventListener("click", () => {
    resetCalculator();
    step5.classList.add("hidden");
    step1.classList.remove("hidden");
  });

  // Show/hide calculations
  showCalculations.addEventListener("change", () => {
    if (showCalculations.checked) {
      calculationDetails.classList.remove("hidden");
    } else {
      calculationDetails.classList.add("hidden");
    }
  });

  // Change description based on shelter class
  shelterClass.addEventListener("change", changeDescription);

  // Wall materials - Load submaterials based on selected material
  wallMaterialType.addEventListener("change", () => loadSubmaterials("wall"));
  wallSubmaterialType.addEventListener("change", () => setThickness("wall"));

  // Roof materials - Load submaterials based on selected material
  roofMaterialType.addEventListener("change", () => loadSubmaterials("roof"));
  roofSubmaterialType.addEventListener("change", () => setThickness("roof"));

  // Step 4 selects
  buildingType.addEventListener("change", loadBuildingsHeight);
  buildingType.addEventListener("change", loadBuildingsDensity);
  buildingType.addEventListener("change", checkStep4Complete);

  buildingHeight.addEventListener("change", checkStep4Complete);
  buildingDensity.addEventListener("change", checkStep4Complete);

  // Thickness validation
  wallThickness.addEventListener("input", () => validateThickness("wall"));
  roofThickness.addEventListener("input", () => validateThickness("roof"));

  resetCalculator();
  loadStorageClasses();
}

// Change description based on selected shelter class
function changeDescription() {
  const shelterClassDescriptionValue =
    shelterClass.options[shelterClass.selectedIndex].getAttribute(
      "data-description"
    );
  const shelterClassCoefficientValue =
    shelterClass.options[shelterClass.selectedIndex].getAttribute(
      "data-coefficient"
    );

  shelterClassDescription.textContent = shelterClassDescriptionValue;
  shelterClassCoefficient.textContent = shelterClassCoefficientValue;
}

function getShelterClassCoefficient() {
  const coefficient =
    shelterClass.options[shelterClass.selectedIndex].getAttribute(
      "data-coefficient"
    );
  return parseFloat(coefficient);
}

// Add wall material to table
function addWallMaterial() {
  if (!validateMaterialForm("wall")) return;

  const material =
    wallMaterialType.options[wallMaterialType.selectedIndex].text;
  const materialId = wallMaterialType.value;
  const thicknessValue = parseInt(wallThickness.value);
  const submaterial =
    wallSubmaterialType.options[wallSubmaterialType.selectedIndex].text;
  const submaterialId = wallSubmaterialType.value;

  const newMaterial = {
    id: calculationData.wallMaterials.length + 1,
    material_id: materialId,
    material: material,
    thickness: thicknessValue,
    submaterial: submaterial,
    sub_material_id: submaterialId,
  };

  calculationData.wallMaterials.push(newMaterial);
  addMaterialRow(newMaterial, wallMaterialsTable, "wall");

  nextToStep3Button.disabled = false;

  const modal = bootstrap.Modal.getInstance(
    document.getElementById("addWallMaterialModal")
  );
  modal.hide();

  wallMaterialType.value = "";
  wallThickness.value = "";
  wallSubmaterialType.value = "";
}

// Add roof material to table
function addRoofMaterial() {
  if (!validateMaterialForm("roof")) return;

  const material =
    roofMaterialType.options[roofMaterialType.selectedIndex].text;
  const materialId = roofMaterialType.value;
  const thicknessValue = parseInt(roofThickness.value);
  const submaterial =
    roofSubmaterialType.options[roofSubmaterialType.selectedIndex].text;
  const submaterialId = roofSubmaterialType.value;

  const newMaterial = {
    id: calculationData.roofMaterials.length + 1,
    material_id: materialId,
    material: material,
    thickness: thicknessValue,
    submaterial: submaterial,
    sub_material_id: submaterialId,
  };

  calculationData.roofMaterials.push(newMaterial);
  addMaterialRow(newMaterial, roofMaterialsTable, "roof");

  nextToStep4Button.disabled = false;

  const modal = bootstrap.Modal.getInstance(
    document.getElementById("addRoofMaterialModal")
  );
  modal.hide();

  roofMaterialType.value = "";
  roofThickness.value = "";
  roofSubmaterialType.value = "";
}

// Add material row to table (universal for wall and roof)
function addMaterialRow(material, tableBody, type) {
  const row = tableBody.insertRow();

  const materialCell = row.insertCell(0);
  const submaterialCell = row.insertCell(1);
  const thicknessCell = row.insertCell(2);
  const actionsCell = row.insertCell(3);

  materialCell.textContent = material.material;
  submaterialCell.textContent = material.submaterial;
  thicknessCell.textContent = material.thickness;

  const deleteButton = document.createElement("button");
  deleteButton.className = "btn btn-sm";
  deleteButton.innerHTML = '<i class="bi bi-trash"></i>';
  deleteButton.onclick = function () {
    deleteMaterial(material.id, row, type);
  };

  actionsCell.appendChild(deleteButton);
}

// Delete material (universal for wall and roof)
function deleteMaterial(id, row, type) {
  const materialsArray =
    type === "wall"
      ? calculationData.wallMaterials
      : calculationData.roofMaterials;
  const tableBody = type === "wall" ? wallMaterialsTable : roofMaterialsTable;
  const nextButton = type === "wall" ? nextToStep3Button : nextToStep4Button;

  const index = materialsArray.findIndex((m) => m.id === id);
  if (index !== -1) {
    materialsArray.splice(index, 1);
  }

  tableBody.removeChild(row);
  reindexMaterials(type);

  if (materialsArray.length === 0) {
    nextButton.disabled = true;
  }
}

// Reindex materials after deletion (universal for wall and roof)
function reindexMaterials(type) {
  const materialsArray =
    type === "wall"
      ? calculationData.wallMaterials
      : calculationData.roofMaterials;
  const tableBody = type === "wall" ? wallMaterialsTable : roofMaterialsTable;

  materialsArray.forEach((material, index) => {
    material.id = index + 1;
  });

  for (let i = 0; i < tableBody.rows.length; i++) {
    tableBody.rows[i].cells[0].textContent = i + 1;
  }
}

// Validate material form (universal for wall and roof)
function validateMaterialForm(type) {
  const materialType = type === "wall" ? wallMaterialType : roofMaterialType;
  const thickness = type === "wall" ? wallThickness : roofThickness;
  const submaterialType =
    type === "wall" ? wallSubmaterialType : roofSubmaterialType;

  if (!materialType.value || !thickness.value || !submaterialType.value) {
    alert("Виберіть матеріал");
    return false;
  }

  return validateThickness(type);
}

// Validate thickness input (universal for wall and roof)
function validateThickness(type) {
  const thicknessInput = type === "wall" ? wallThickness : roofThickness;
  const thicknessValue = parseInt(thicknessInput.value);

  if (
    isNaN(thicknessValue) ||
    thicknessValue < 10 ||
    thicknessValue > 150 ||
    thicknessValue % 5 !== 0
  ) {
    thicknessInput.classList.add("is-invalid");
    return false;
  } else {
    thicknessInput.classList.remove("is-invalid");
    return true;
  }
}

// Go to step 2
function goToStep2() {
  step1.classList.add("hidden");
  step2.classList.remove("hidden");

  calculationData.az = getShelterClassCoefficient();
  loadMaterials("wall");
}

// Go to step 3
function goToStep3() {
  step2.classList.add("hidden");
  step3.classList.remove("hidden");

  loadMaterials("roof");
}

// Go to step 4
function goToStep4() {
  step3.classList.add("hidden");
  step4.classList.remove("hidden");

  loadBuildingTypes();
}

// Check if step 4 is complete
function checkStep4Complete() {
  if (buildingHeight.value && buildingDensity.value) {
    calculateButton.disabled = false;
  } else {
    calculateButton.disabled = true;
  }
}

function showCalculationsDetails(data) {
  console.log("Calculation result:", data);

  const az = data.az;
  const kzab = Math.round(data.kzab * 1000) / 1000;
  const kbud = Math.round(data.kbud * 1000) / 1000;

  // Wall calculations
  const kyWall = Math.round(data.ky_wall * 1000) / 1000;
  const knWall = Math.round(data.kn_wall * 1000) / 1000;
  const KNWall = Math.round(data.KN_WALL * 1000) / 1000;
  const azfWall = Math.round(data.AZF_WALL * 1000) / 1000;

  // Roof calculations
  const kyRoof = Math.round(data.ky_roof * 1000) / 1000;
  const knRoof = Math.round(data.kn_roof * 1000) / 1000;
  const KNRoof = Math.round(data.KN_ROOF * 1000) / 1000;
  const azfRoof = Math.round(data.AZF_ROOF * 1000) / 1000;

  // Display wall results
  expectedProtectionWall.textContent = az;
  calculatedProtectionWall.textContent = azfWall;

  // Display roof results
  expectedProtectionRoof.textContent = az;
  calculatedProtectionRoof.textContent = azfRoof;

  // Show calculation details for wall
  const calculationResultsWall = document.getElementById(
    "calculationResultsWall"
  );
  calculationResultsWall.textContent = `${az} <= ${azfWall} = 1.18 × (${kyWall} × ${knWall}) × (${kzab} / ${kbud}) × ${KNWall} / (${kyWall} + ${knWall})`;

  // Show calculation details for roof
  const calculationResultsRoof = document.getElementById(
    "calculationResultsRoof"
  );
  calculationResultsRoof.textContent = `${az} <= ${azfRoof} = 1.18 × (${kyRoof} × ${knRoof}) × (${kzab} / ${kbud}) × ${KNRoof} / (${kyRoof} + ${knRoof})`;

  // Show warnings if protection is insufficient
  if (az > azfWall) {
    resultWarningWall.classList.remove("hidden");
  } else {
    resultWarningWall.classList.add("hidden");
  }

  if (az > azfRoof) {
    resultWarningRoof.classList.remove("hidden");
  } else {
    resultWarningRoof.classList.add("hidden");
  }
}

// Calculate results
function calculateResults() {
  calculationData.buildingParams = {
    height: buildingHeight.value,
    density: buildingDensity.value,
    type_id: buildingType.value,
  };
  console.log("calculationData:", calculationData);

  const dataPayload = {
    az: calculationData.az,
    wall_materials: calculationData.wallMaterials,
    roof_materials: calculationData.roofMaterials,
    building_type_id: calculationData.buildingParams.type_id,
    building_height: calculationData.buildingParams.height,
    building_density: calculationData.buildingParams.density,
  };
  console.log("dataPayload:", dataPayload);

  const calculateUrl = `${baseUrl}/api/calculations/azf`;
  fetch(calculateUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataPayload),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      showCalculationsDetails(data);

      step4.classList.add("hidden");
      step5.classList.remove("hidden");
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

// Reset calculator
function resetCalculator() {
  calculationData.wallMaterials = [];
  calculationData.roofMaterials = [];
  calculationData.buildingType = "";
  calculationData.buildingParams = {};

  // Clear wall materials table
  while (wallMaterialsTable.rows.length > 0) {
    wallMaterialsTable.deleteRow(0);
  }

  // Clear roof materials table
  while (roofMaterialsTable.rows.length > 0) {
    roofMaterialsTable.deleteRow(0);
  }

  // Reset wall form values
  wallMaterialType.value = "";
  wallThickness.value = "";
  wallSubmaterialType.value = "";

  // Reset roof form values
  roofMaterialType.value = "";
  roofThickness.value = "";
  roofSubmaterialType.value = "";

  // Reset building parameters
  buildingType.value = "";
  buildingHeight.value = "";
  buildingDensity.value = "";

  // Disable buttons
  nextToStep3Button.disabled = true;
  nextToStep4Button.disabled = true;
  calculateButton.disabled = true;

  // Hide calculation details
  showCalculations.checked = false;
  resultWarningWall.classList.add("hidden");
  resultWarningRoof.classList.add("hidden");
  calculationDetails.classList.add("hidden");
}

// Initialize application
document.addEventListener("DOMContentLoaded", init);

function loadStorageClasses() {
  const storageClassesUrl = `${baseUrl}/api/storage-classes`;

  fetch(storageClassesUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const shelterClassSelect = document.getElementById("shelterClass");
      data.forEach((shelterClassItem) => {
        const option = document.createElement("option");
        option.value = shelterClassItem.id;
        option.textContent = shelterClassItem.protection_class;
        option.setAttribute("data-description", shelterClassItem.description);
        option.setAttribute(
          "data-coefficient",
          shelterClassItem.radiation_protection_level
        );
        shelterClassSelect.appendChild(option);
      });
      shelterClassSelect.value = data[0].id;
      changeDescription();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function loadMaterials(type) {
  const materialsUrl = `${baseUrl}/api/materials`;
  const materialTypeSelect =
    type === "wall" ? wallMaterialType : roofMaterialType;

  fetch(materialsUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      materialTypeSelect.innerHTML = "";

      data.forEach((materialItem) => {
        const option = document.createElement("option");
        option.value = materialItem.id;
        option.textContent = materialItem.name;
        materialTypeSelect.appendChild(option);
      });

      materialTypeSelect.value = data[0].id;
      loadSubmaterials(type);
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

// Load submaterials (universal for wall and roof)
function loadSubmaterials(type) {
  const materialTypeSelect =
    type === "wall" ? wallMaterialType : roofMaterialType;
  const submaterialTypeSelect =
    type === "wall" ? wallSubmaterialType : roofSubmaterialType;

  const subMaterialsUrl = `${baseUrl}/api/materials/${materialTypeSelect.value}/sub-materials`;

  fetch(subMaterialsUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      submaterialTypeSelect.innerHTML = "";

      data.forEach((submaterialItem) => {
        const option = document.createElement("option");
        option.value = submaterialItem.id;
        option.textContent = submaterialItem.display_name;
        option.setAttribute(
          "data-minimum_thickness",
          submaterialItem.minimum_thickness
        );
        option.setAttribute(
          "data-maximum_thickness",
          submaterialItem.maximum_thickness
        );
        submaterialTypeSelect.appendChild(option);
      });

      setThickness(type);
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function setThickness(type) {
  const submaterialTypeSelect =
    type === "wall" ? wallSubmaterialType : roofSubmaterialType;
  const thicknessInput = type === "wall" ? wallThickness : roofThickness;

  const minThickness = submaterialTypeSelect.options[
    submaterialTypeSelect.selectedIndex
  ].getAttribute("data-minimum_thickness");
  const maxThickness = submaterialTypeSelect.options[
    submaterialTypeSelect.selectedIndex
  ].getAttribute("data-maximum_thickness");

  thicknessInput.setAttribute("min", minThickness);
  thicknessInput.setAttribute("max", maxThickness);
  thicknessInput.value = minThickness;
  validateThickness(type);
}

function loadBuildingTypes() {
  const buildingTypesUrl = `${baseUrl}/api/building-types`;

  fetch(buildingTypesUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const buildingTypeSelect = document.getElementById("buildingType");
      buildingTypeSelect.innerHTML = "";

      data.forEach((buildingTypeItem) => {
        const option = document.createElement("option");
        option.value = buildingTypeItem.id;
        option.textContent = buildingTypeItem.name;
        buildingTypeSelect.appendChild(option);
      });

      buildingTypeSelect.value = data[0].id;
      loadBuildingsHeight();
      loadBuildingsDensity();
      checkStep4Complete();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function loadBuildingsHeight() {
  const buildingTypeId = buildingType.value;
  const buildingHeightUrl = `${baseUrl}/api/building-types/${buildingTypeId}/buildings-height`;

  fetch(buildingHeightUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const buildingHeightSelect = document.getElementById("buildingHeight");
      buildingHeightSelect.innerHTML = "";

      data.forEach((buildingHeightItem) => {
        const option = document.createElement("option");
        option.value = buildingHeightItem;
        option.textContent = buildingHeightItem;
        buildingHeightSelect.appendChild(option);
      });

      buildingHeightSelect.value = data[0];
      checkStep4Complete();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function loadBuildingsDensity() {
  const buildingTypeId = buildingType.value;
  const buildingDensityUrl = `${baseUrl}/api/building-types/${buildingTypeId}/buildings-density`;

  fetch(buildingDensityUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const buildingDensitySelect = document.getElementById("buildingDensity");
      buildingDensitySelect.innerHTML = "";

      data.forEach((buildingDensityItem) => {
        const option = document.createElement("option");
        option.value = buildingDensityItem;
        option.textContent = buildingDensityItem;
        buildingDensitySelect.appendChild(option);
      });

      buildingDensitySelect.value = data[0];
      checkStep4Complete();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}
