document.addEventListener("DOMContentLoaded", function () {
    const airlineDropdown = document.getElementById("marketing_airline_name");
    const flightDropdown = document.getElementById("marketing_flight_num");

    airlineDropdown.addEventListener("change", function () {
        const airline = airlineDropdown.value;

        flightDropdown.innerHTML = '<option value="">Loading...</option>';

        if (!airline) {
            flightDropdown.innerHTML = '<option value="">Select airline first</option>';
            return;
        }

        fetch(`/get_in_progress_flights?marketing_airline_name=${encodeURIComponent(airline)}`)
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                flightDropdown.innerHTML = '<option value="">Select flight</option>';

                if (data.flights.length === 0) {
                    flightDropdown.innerHTML = '<option value="">No in-progress flights found</option>';
                    return;
                }

                data.flights.forEach(function (flight) {
                    const option = document.createElement("option");

                    option.value = flight.marketing_flight_num;

                    option.textContent =
                        flight.marketing_airline_name + " " +
                        flight.marketing_flight_num +
                        " → operating " +
                        flight.operating_airline_name + " " +
                        flight.flight_number;

                    flightDropdown.appendChild(option);
                });
            })
            .catch(function (error) {
                console.log("Error loading flights:", error);
                flightDropdown.innerHTML = '<option value="">Error loading flights</option>';
            });
    });
});