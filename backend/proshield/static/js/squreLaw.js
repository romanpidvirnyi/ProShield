document
  .getElementById("calculationType")
  .addEventListener("change", function () {
    const sections = {
      default: "defaultSection",
      known_source: "knownSourceSection",
      one_measurement: "oneMeasurementSection",
      two_measurements: "twoMeasurementsSection",
    };

    Object.values(sections).forEach((sectionId) => {
      document.getElementById(sectionId).style.display = "none";
    });

    if (this.value === "default") {
      document.getElementById("calculateBtn").style.display = "none";
    } else {
      document.getElementById("calculateBtn").style.display = "block";
    }

    document.getElementById("resultSection").style.display = "none";
    document.getElementById(sections[this.value]).style.display = "block";
  });

document.getElementById("calculateBtn").addEventListener("click", function () {
  const calculationType = document.getElementById("calculationType").value;
  let result = undefined;

  switch (calculationType) {
    case "known_source":
      result = calculateKnownSource();
      break;
    case "one_measurement":
      result = calculateOneMeasurement();
      break;
    case "two_measurements":
      result = calculateTwoMeasurements();
      break;
  }

  if (!result) return;

  const resultSection = document.getElementById("resultSection");
  const resultText = document.getElementById("resultText");
  resultText.innerHTML = result;
  resultSection.style.display = "block";
});

function calculateKnownSource() {
  const referenceYear = document.getElementById("referenceYear").value;
  const referenceActivity = document.getElementById("referenceActivity").value;
  const referenceActivityUnit = document.getElementById(
    "referenceActivityUnit"
  ).value;
  const radioactiveMaterial = document.getElementById(
    "radioactiveMaterial"
  ).value;

  const radioactiveMaterialOptions = document.getElementById(
    "radioactiveMaterial"
  ).options;
  const radioactiveMaterialOptionsArray = Array.from(
    radioactiveMaterialOptions
  );
  const radioactiveMaterialHalflifeY = radioactiveMaterialOptionsArray
    .find((option) => option.value === radioactiveMaterial)
    .getAttribute("data-halflifeY");
  console.log(
    "radioactiveMaterialhalflifeY",
    Number(radioactiveMaterialHalflifeY)
  );
  const radioactiveMaterialGamma = radioactiveMaterialOptionsArray
    .find((option) => option.value === radioactiveMaterial)
    .getAttribute("data-gamma");
  console.log("radioactiveMaterialGamma", Number(radioactiveMaterialGamma));

  const currentYear = new Date().getFullYear();

  if (
    !validateNumberInput(referenceActivity, "Покази приладу") ||
    !validateYear(referenceYear, "Довідковий час")
  )
    return;

  // TODO: implement proper calculation
  const yearsPassed = currentYear - referenceYear;
  const decayRate = referenceYear;

  const dose1 = 1e-4; // 100 мкЗв/год = 1e-4 Зв/год
  const dose2 = 1e-6; // 1 мкЗв/год = 1e-6 Зв/год

  console.log(radioactiveMaterialGamma);
  const hotZone = Math.sqrt(
    (referenceActivity * radioactiveMaterialGamma * 1e9) / dose1
  );
  const warmZone = Math.sqrt(
    (referenceActivity * radioactiveMaterialGamma * 1e9) / dose2
  );

  // TODO: RESULTS
  resetInfographic();
  document.getElementById("warmZoneLabel").innerHTML = `${warmZone} м`;
  document.getElementById("hotZoneLabel").innerHTML = `${hotZone} м`;

  return `
    <p>Відстань до пекельної зони (100 мкЗв/рік): ${hotZone} м</p>
    <p>Відстань до гарячої зони (1 мкЗв/рік): ${warmZone} м</p>
  `;
}

function calculateOneMeasurement() {
  const sourceDistance = document.getElementById("sourceDistance").value;
  const dosePower = document.getElementById("dosePower").value;
  const dosePowerUnit = document.getElementById("dosePowerUnit").value;

  if (
    !validateNumberInput(
      sourceDistance,
      "Відстань до джерела випромінювання"
    ) ||
    !validateNumberInput(dosePower, "Виміряна потужність дози")
  )
    return;

  // TODO: implement proper calculation
  const hotZone = sourceDistance * Math.sqrt(dosePower / 100) * 1; // koef UM
  const warmZone = sourceDistance * Math.sqrt(dosePower / 1) * 1;

  resetInfographic();
  document.getElementById("warmZoneLabel").innerHTML = `${warmZone} м`;
  document.getElementById("hotZoneLabel").innerHTML = `${hotZone} м`;
  document.getElementById("firefighter1").style.display = "block";
  document.getElementById("firefighterLabel1").style.display = "block";
  document.getElementById(
    "firefighterLabel1"
  ).innerHTML = `${dosePower}<br>${dosePowerUnit}`;
  document.getElementById("sourceDistanceLabel").style.display = "block";
  document.getElementById(
    "sourceDistanceLabel"
  ).innerHTML = `${sourceDistance} м`;

  return `
    <p>Відстань до пекельної зони (100 мкЗв/рік): ${hotZone} м</p>
    <p>Відстань до гарячої зони (1 мкЗв/рік): ${warmZone} м</p>
  `;
}

function calculateTwoMeasurements() {
  const distanceBetween = document.getElementById("distanceBetween").value;
  var dosePower1 = document.getElementById("dosePower1").value;
  const dosePowerUnit1 = document.getElementById("dosePowerUnit1").value;
  var dosePower2 = document.getElementById("dosePower2").value;
  const dosePowerUnit2 = document.getElementById("dosePowerUnit2").value;

  if (
    !validateNumberInput(distanceBetween, "Відстань між вимірюваннями") ||
    !validateNumberInput(dosePower1, "Виміряна потужність дози (1)") ||
    !validateNumberInput(dosePower2, "Виміряна потужність дози (2)")
  )
    return;

  // TODO: implement proper calculation
  console.log("dosePower1", dosePower1);
  console.log("dosePower2", dosePower2);
  if (dosePower1 > dosePower2) {
    var tempDosePower = dosePower1;
    dosePower1 = dosePower2;
    dosePower2 = tempDosePower;
  }
  console.log("dosePower1", dosePower1);
  console.log("dosePower2", dosePower2);

  var ratio = Math.sqrt(dosePower1 / dosePower2);
  const distanceTo = (-distanceBetween * ratio) / (ratio - 1);

  const hotZone = distanceBetween / 1000;
  const warmZone = distanceBetween / 100;

  resetInfographic();
  document.getElementById("warmZoneLabel").innerHTML = `${warmZone} м`;
  document.getElementById("hotZoneLabel").innerHTML = `${hotZone} м`;
  document.getElementById("firefighter1").style.display = "block";
  document.getElementById("firefighter2").style.display = "block";
  document.getElementById("firefighterLabel1").style.display = "block";
  document.getElementById("firefighterLabel2").style.display = "block";
  document.getElementById(
    "firefighterLabel1"
  ).innerHTML = `${dosePower2}<br>${dosePowerUnit2}`;
  document.getElementById(
    "firefighterLabel2"
  ).innerHTML = `${dosePower1}<br>${dosePowerUnit1}`;
  document.getElementById("sourceDistanceLabel").style.display = "block";
  document.getElementById("sourceDistanceLabel").innerHTML = `${distanceTo} м`;
  document.getElementById("distanceBetweenLabel").style.display = "block";
  document.getElementById(
    "distanceBetweenLabel"
  ).innerHTML = `${distanceBetween} м`;

  return `
    <p>Джерело випромінювання розташоване на відстані ${distanceBetween} м від найближчої точки вимірювання</p>
    <p>Відстань до пекельної зони (100 мкЗв/рік): ${hotZone} м</p>
    <p>Відстань до гарячої зони (1 мкЗв/рік): ${warmZone} м</p>
  `;
}

function resetInfographic() {
  document.getElementById("warmZoneLabel").innerHTML = "";
  document.getElementById("hotZoneLabel").innerHTML = "";
  document.getElementById("firefighter1").style.display = "none";
  document.getElementById("firefighter2").style.display = "none";
  document.getElementById("firefighterLabel1").style.display = "none";
  document.getElementById("firefighterLabel2").style.display = "none";
  document.getElementById("sourceDistanceLabel").style.display = "none";
  document.getElementById("distanceBetweenLabel").style.display = "none";
}

function validateNumberInput(input, fieldName) {
  // Remove any whitespace
  const value = input.trim();

  // Check if empty (required validation)
  if (!value) {
    alert(`Error: ${fieldName} is required.`);
    return false;
  }

  // Convert to number and check if it's valid
  const numberValue = Number(value);

  // Check if it's NaN (Not a Number)
  if (isNaN(numberValue)) {
    alert(`Error: ${fieldName} must be a valid number.`);
    return false;
  }

  // All validations passed
  return true;
}

function validateYear(yearString, fieldName = "Year") {
  // Remove any whitespace
  const value = yearString.trim();

  // Check if empty
  if (!value) {
    alert(`Error: ${fieldName} is required.`);
    return false;
  }

  // Check if it matches the YYYY format using a regular expression
  const yearRegex = /^\d{4}$/;
  if (!yearRegex.test(value)) {
    alert(`Error: ${fieldName} must be in YYYY format.`);
    return false;
  }

  // Convert to number
  const yearValue = Number(value);

  // Get current year
  const currentYear = new Date().getFullYear();

  // Check if year is smaller than current year
  if (yearValue >= currentYear) {
    alert(`Error: ${fieldName} must be earlier than ${currentYear}.`);
    return false;
  }

  // All validations passed
  return true;
}
