window.addEventListener("load", () => {
    console.log("MODIFYING DIMENSION")
    const typeSelect = document.getElementById('id_type')
    const lengthInput = document.getElementById("id_length")
    const breadthInput = document.getElementById("id_breadth")
    const widthInput = document.getElementById("id_width")
    const thicknessInput = document.getElementById("id_thickness")
    const diameterInput = document.getElementById("id_diameter")

    const allInputs = [
        lengthInput, breadthInput, widthInput, thicknessInput, diameterInput
    ]
    allInputs.forEach(function (input) {
        // input.style.display = 'none'
        input.parentNode.parentElement.style.display = 'none';
    })
    function switchInputs(offArray, onArray) {
        offArray.forEach((input) => {
            input.parentNode.parentElement.style.display = 'none';
        })
        onArray.forEach((input) => {
            input.parentNode.parentElement.style.display = 'block'
        })
    }
    typeSelect.addEventListener('change', (e) => {
        let v = e.target.value;
        if (v == "0") {
            switchInputs([thicknessInput, diameterInput], [lengthInput, breadthInput, widthInput])
        } else if (v == "1") {
            switchInputs([breadthInput, diameterInput], [lengthInput, thicknessInput, widthInput])
        } else if (v == "2") {
            switchInputs([breadthInput, thicknessInput, diameterInput], [lengthInput, widthInput])
        } else {
            allInputs.forEach(function (input) {
                input.parentNode.parentElement.style.display = 'none';
            })
        }
    })
})
