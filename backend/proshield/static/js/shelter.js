// Global data storage
const calculationData = {
  az: "",
  materials: [],
  buildingType: "",
  buildingParams: {},
};

// DOM elements
const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");
const step4 = document.getElementById("step4");

const shelterClass = document.getElementById("shelterClass");
const shelterClassDescription = document.getElementById(
  "shelterClassDescription"
);
const shelterClassCoefficient = document.getElementById(
  "shelterClassCoefficient"
);

const materialsTable = document
  .getElementById("materialsTable")
  .getElementsByTagName("tbody")[0];
const nextToStep2Button = document.getElementById("nextToStep2Button");
const nextToStep3Button = document.getElementById("nextToStep3Button");
const calculateButton = document.getElementById("calculateButton");

const backToStep1Button = document.getElementById("backToStep1Button");
const backToStep2Button = document.getElementById("backToStep2Button");
const backToStep3Button = document.getElementById("backToStep3Button");
const backToStep4Button = document.getElementById("backToStep4Button");
const startOverButton = document.getElementById("startOverButton");

const buildingType = document.getElementById("buildingType");
const buildingHeight = document.getElementById("buildingHeight");
const buildingDensity = document.getElementById("buildingDensity");

const addMaterialForm = document.getElementById("addMaterialForm");
const materialType = document.getElementById("materialType");
const thickness = document.getElementById("thickness");
const submaterialType = document.getElementById("submaterialType");
const saveMaterialButton = document.getElementById("saveMaterialButton");

const resultWarning = document.getElementById("resultWarning");
const expectedProtection = document.getElementById("expectedProtection");
const calculatedProtection = document.getElementById("calculatedProtection");
const showCalculations = document.getElementById("showCalculations");
const calculationDetails = document.getElementById("calculationDetails");

// Get HOST URL for api requests
const baseUrl = window.location.origin;

// Initialize
function init() {
  // Add Material Modal
  saveMaterialButton.addEventListener("click", addMaterial);

  // Navigation buttons
  nextToStep2Button.addEventListener("click", goToStep2);
  nextToStep3Button.addEventListener("click", goToStep3);
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

  startOverButton.addEventListener("click", () => {
    resetCalculator();
    step4.classList.add("hidden");
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

  // Chnge description based on shelter class
  shelterClass.addEventListener("change", changeDescription);

  // Load submaterials based on selected material
  materialType.addEventListener("change", loadSubmaterials);
  submaterialType.addEventListener("change", setThickness);

  // Step 3 selects
  buildingType.addEventListener("change", loadBuildingsHeight);
  buildingType.addEventListener("change", loadBuildingsDensity);
  buildingType.addEventListener("change", checkStep3Complete);

  buildingHeight.addEventListener("change", checkStep3Complete);
  buildingDensity.addEventListener("change", checkStep3Complete);

  // Thickness validation
  thickness.addEventListener("input", validateThickness);

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
  const shelterClassCoefficient =
    shelterClass.options[shelterClass.selectedIndex].getAttribute(
      "data-coefficient"
    );

  return parseFloat(shelterClassCoefficient);
}

// Add material to table
function addMaterial() {
  if (!validateMaterialForm()) return;

  const material = materialType.options[materialType.selectedIndex].text;
  const materialId = materialType.value;
  const thicknessValue = parseInt(thickness.value);
  const submaterial =
    submaterialType.options[submaterialType.selectedIndex].text;
  const submaterialId = submaterialType.value;

  // Create new material object
  const newMaterial = {
    id: calculationData.materials.length + 1,
    material_id: materialId,
    material: material,
    thickness: thicknessValue,
    submaterial: submaterial,
    sub_material_id: submaterialId,
  };

  // Add to data storage
  calculationData.materials.push(newMaterial);

  // Add to table
  addMaterialRow(newMaterial);

  // Enable next button if we have at least one material
  nextToStep3Button.disabled = false;

  // Close modal and reset form
  const modal = bootstrap.Modal.getInstance(
    document.getElementById("addMaterialModal")
  );
  modal.hide();

  materialType.value = "";
  thickness.value = "";
  submaterialType.value = "";
}

// Add material row to table
function addMaterialRow(material) {
  const row = materialsTable.insertRow();

  const materialCell = row.insertCell(0);
  const submaterialCell = row.insertCell(1);
  const thicknessCell = row.insertCell(2);
  const actionsCell = row.insertCell(3);

  materialCell.textContent = material.material;
  submaterialCell.textContent = material.submaterial;
  thicknessCell.textContent = material.thickness;

  // Delete button
  const deleteButton = document.createElement("button");
  deleteButton.className = "btn btn-sm";
  deleteButton.innerHTML = '<i class="bi bi-trash"></i>';
  deleteButton.onclick = function () {
    deleteMaterial(material.id, row);
  };

  actionsCell.appendChild(deleteButton);
}

// Delete material
function deleteMaterial(id, row) {
  // Remove from data storage
  const index = calculationData.materials.findIndex((m) => m.id === id);
  if (index !== -1) {
    calculationData.materials.splice(index, 1);
  }

  // Remove row from table
  materialsTable.removeChild(row);

  // Re-index remaining materials
  reindexMaterials();

  // Disable next button if no materials
  if (calculationData.materials.length === 0) {
    nextToStep3Button.disabled = true;
  }
}

// Reindex materials after deletion
function reindexMaterials() {
  // Update data storage IDs
  calculationData.materials.forEach((material, index) => {
    material.id = index + 1;
  });

  // Update table IDs
  for (let i = 0; i < materialsTable.rows.length; i++) {
    materialsTable.rows[i].cells[0].textContent = i + 1;
  }
}

// Validate material form
function validateMaterialForm() {
  if (!materialType.value || !thickness.value || !submaterialType.value) {
    alert("Виберіть матеріал");
    return false;
  }

  return validateThickness();
}

// Validate thickness input
function validateThickness() {
  const thicknessValue = parseInt(thickness.value);

  if (
    isNaN(thicknessValue) ||
    thicknessValue < 10 ||
    thicknessValue > 150 ||
    thicknessValue % 5 !== 0
  ) {
    thickness.classList.add("is-invalid");
    return false;
  } else {
    thickness.classList.remove("is-invalid");
    return true;
  }
}

// Go to step 2
function goToStep2() {
  step1.classList.add("hidden");
  step2.classList.remove("hidden");

  // Save shelter class coefficient
  calculationData.az = getShelterClassCoefficient();

  // get materials for step 3
  loadMaterials();
}

// Go to step 3
function goToStep3() {
  step2.classList.add("hidden");
  step3.classList.remove("hidden");

  loadBuildingTypes();
}

// Check if step 4 is complete
function checkStep3Complete() {
  if (buildingHeight.value && buildingDensity.value) {
    calculateButton.disabled = false;
  } else {
    calculateButton.disabled = true;
  }
}

function showCalculationsDetails(data) {
  console.log("Calculation result:", data);
  const expectedProtectionValue = data.az; // data.expectedProtection;
  const calculatedProtectionValue = Math.round(data.AZF * 1000) / 1000; // data.calculatedProtection;

  expectedProtection.textContent = expectedProtectionValue;
  calculatedProtection.textContent = calculatedProtectionValue;
  // Show calculation results
  const calculationResults = document.getElementById("calculationResults");
  // АЗ ≤ АЗФ = 1,18 (Ky,i × Kn,i) × Kp × KN / (Ky,i + Kn,i),
  calculationResults.textContent = `${expectedProtectionValue} <= ${calculatedProtectionValue} = 1.18 (${data.ky} x ${data.kn}) x (${data.kzab} / ${data.kbud}) x ${data.KN} / (${data.ky} + ${data.kn})`;
  if (expectedProtectionValue > calculatedProtectionValue) {
    resultWarning.classList.remove("hidden");
  }
}
// Calculate results
function calculateResults() {
  // Save building parameters
  calculationData.buildingParams = {
    height: buildingHeight.value,
    density: buildingDensity.value,
    type_id: buildingType.value,
  };
  console.log("calculationData:", calculationData);

  const dataPayload = {
    az: calculationData.az,
    materials: calculationData.materials,
    building_type_id: calculationData.buildingParams.type_id,
    building_height: calculationData.buildingParams.height,
    building_density: calculationData.buildingParams.density,
  };
  console.log("dataPayload:", dataPayload);

  const calculateUrl = `${baseUrl}/api/calculations/azf`;
  console.log("data:", dataPayload);
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

      step3.classList.add("hidden");
      step4.classList.remove("hidden");
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

// Reset calculator
function resetCalculator() {
  // Clear data storage
  calculationData.materials = [];
  calculationData.buildingType = "";
  calculationData.buildingParams = {};

  // Clear table
  while (materialsTable.rows.length > 0) {
    materialsTable.deleteRow(0);
  }

  // Reset form values
  materialType.value = "";
  thickness.value = "";
  submaterialType.value = "";
  buildingType.value = "";
  buildingHeight.value = "";
  buildingDensity.value = "";

  // Disable buttons
  nextToStep3Button.disabled = true;
  calculateButton.disabled = true;

  // Hide calculation details
  showCalculations.checked = false;
  resultWarning.classList.add("hidden");
  calculationDetails.classList.add("hidden");
}

// Mock API request
function mockApiRequest(endpoint, data) {
  return new Promise((resolve) => {
    console.log(`Sending data to ${endpoint}:`, data);

    // Simulate API delay
    setTimeout(() => {
      resolve({ status: "success" });
    }, 500);
  });
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
      // Set default value
      shelterClassSelect.value = data[0].id;
      changeDescription();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function loadMaterials() {
  const materialsUrl = `${baseUrl}/api/materials`;

  fetch(materialsUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const materialTypeSelect = document.getElementById("materialType");
      materialTypeSelect.innerHTML = "";

      data.forEach((materialItem) => {
        const option = document.createElement("option");
        option.value = materialItem.id;
        option.textContent = materialItem.name;
        materialTypeSelect.appendChild(option);
      });
      // Set default value
      materialTypeSelect.value = data[0].id;
      loadSubmaterials();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

// Load submaterials
function loadSubmaterials() {
  const materialTypeSelect = document.getElementById("materialType");
  const subMaterialsUrl = `${baseUrl}/api/materials/${materialTypeSelect.value}/sub-materials`;
  fetch(subMaterialsUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const submaterialTypeSelect = document.getElementById("submaterialType");
      submaterialTypeSelect.innerHTML = ""; // Clear previous options
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
      // Set min and max values for thickness
      setThickness();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}

function setThickness() {
  const minThickness = submaterialType.options[
    submaterialType.selectedIndex
  ].getAttribute("data-minimum_thickness");
  const maxThickness = submaterialType.options[
    submaterialType.selectedIndex
  ].getAttribute("data-maximum_thickness");

  thickness.setAttribute("min", minThickness);
  thickness.setAttribute("max", maxThickness);
  thickness.value = minThickness;
  validateThickness();
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
      // clear select options
      buildingTypeSelect.innerHTML = "";

      data.forEach((buildingTypeItem) => {
        const option = document.createElement("option");
        option.value = buildingTypeItem.id;
        option.textContent = buildingTypeItem.name;
        buildingTypeSelect.appendChild(option);
      });
      // Set default value
      buildingTypeSelect.value = data[0].id;
      loadBuildingsHeight();
      loadBuildingsDensity();
      checkStep3Complete();
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
      // clear select options
      buildingHeightSelect.innerHTML = "";

      data.forEach((buildingHeightItem) => {
        const option = document.createElement("option");
        option.value = buildingHeightItem;
        option.textContent = buildingHeightItem;
        buildingHeightSelect.appendChild(option);
      });
      // Set default value
      buildingHeightSelect.value = data[0];
      checkStep3Complete();
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
      // clear select options
      buildingDensitySelect.innerHTML = "";

      data.forEach((buildingDensityItem) => {
        const option = document.createElement("option");
        option.value = buildingDensityItem;
        option.textContent = buildingDensityItem;
        buildingDensitySelect.appendChild(option);
      });
      // Set default value
      buildingDensitySelect.value = data[0];
      checkStep3Complete();
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}
