<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AKAS // Global HCHO & AQI Intelligence Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Space+Mono:wght@400;700&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .mono { font-family: 'Space Mono', monospace; }
        #map-canvas { height: 500px; width: 100%; transition: all 0.3s ease; }
        .custom-glass { background: rgba(30, 41, 59, 0.75); backdrop-filter: blur(16px); }
    </style>
</head>
<body class="bg-[#0b0f19] text-slate-100 min-h-screen selection:bg-cyan-500 selection:text-black">

    <div class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
        
        <!-- App Header -->
        <header class="flex flex-col md:flex-row md:items-center md:justify-between border-b border-slate-800 pb-6 gap-4">
            <div>
                <div class="flex items-center gap-2">
                    <span class="h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
                    <h1 class="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">AKAS NETWORKS</h1>
                </div>
                <p class="text-xs text-slate-400 mt-1 uppercase tracking-widest mono">Atmospheric Pollution & Environmental Analytics Dashboard v1.0</p>
            </div>
            
            <button onclick="triggerBrowserGeolocation()" class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold px-5 py-3 rounded-xl flex items-center gap-2 shadow-lg shadow-cyan-950/40 transition active:scale-95">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" /></svg>
                Track My Live Location
            </button>
        </header>

        <!-- Primary Workspace Architecture Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Metric Engine Sidebar Display -->
            <div class="lg:col-span-1 space-y-4 flex flex-col justify-between">
                
                <!-- Target Station Banner card -->
                <div class="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl custom-glass">
                    <span class="text-[10px] font-bold text-cyan-400 bg-cyan-950/60 border border-cyan-800 px-2 py-0.5 rounded-md uppercase tracking-wider mono">Active Telemetry Grid Node</span>
                    <h2 id="ui-station" class="text-xl font-bold text-white mt-2 truncate">Global Static Viewport</h2>
                    <p id="ui-attribution" class="text-xs text-slate-500 mt-0.5 truncate">Click anywhere on the map grid to query data</p>
                </div>

                <!-- Main Scalar Core Value Monitor -->
                <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl flex items-center justify-between shadow-xl custom-glass">
                    <div>
                        <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Holistic Air Quality Index</p>
                        <p id="ui-interpretation" class="text-sm text-slate-300 font-semibold mt-1">Awaiting Data Ingestion</p>
                    </div>
                    <div class="text-right">
                        <span id="ui-aqi" class="text-6xl font-black text-slate-600 transition-colors duration-300">--</span>
                    </div>
                </div>

                <!-- Secondary Sensor Arrays -->
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-slate-900/40 border border-slate-800/80 p-4 rounded-2xl">
                        <span class="text-xs text-slate-400 block">Formaldehyde (HCHO)</span>
                        <span id="ui-hcho" class="text-xl font-bold text-cyan-400 tracking-tight block mt-1">--</span>
                        <span id="ui-risk-badge" class="text-[10px] text-slate-500 font-bold uppercase block mt-0.5">Risk Level: --</span>
                    </div>
                    <div class="bg-slate-900/40 border border-slate-800/80 p-4 rounded-2xl">
                        <span class="text-xs text-slate-400 block">Fine Matter (PM2.5)</span>
                        <span id="ui-pm25" class="text-xl font-bold text-white tracking-tight block mt-1">--</span>
                        <span class="text-[10px] text-slate-500 block mt-0.5">Micro-particles</span>
                    </div>
                    <div class="bg-slate-900/40 border border-slate-800/80 p-4 rounded-2xl">
                        <span class="text-xs text-slate-400 block">Nitrogen Dioxide (NO2)</span>
                        <span id="ui-no2" class="text-xl font-bold text-white tracking-tight block mt-1">--</span>
                    </div>
                    <div class="bg-slate-900/40 border border-slate-800/80 p-4 rounded-2xl">
                        <span class="text-xs text-slate-400 block">Ambient Temperature</span>
                        <span id="ui-temp" class="text-xl font-bold text-emerald-400 tracking-tight block mt-1">--</span>
                    </div>
                </div>

                <!-- Manual Latitude / Longitude input override deck -->
                <div class="bg-slate-900/30 border border-slate-800/60 p-4 rounded-2xl space-y-3">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mono">Manual Coordinate Overrides</p>
                    <div class="grid grid-cols-2 gap-2">
                        <input id="input-lat" type="number" step="0.0001" placeholder="Latitude" class="bg-slate-950 border border-slate-800 text-white text-sm rounded-xl p-2.5 outline-none focus:border-cyan-500 transition w-full">
                        <input id="input-lon" type="number" step="0.0001" placeholder="Longitude" class="bg-slate-950 border border-slate-800 text-white text-sm rounded-xl p-2.5 outline-none focus:border-cyan-500 transition w-full">
                    </div>
                    <button onclick="executeManualQuery()" class="w-full bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold py-2.5 rounded-xl border border-slate-700 transition">Execute Scan Check</button>
                </div>
            </div>

            <!-- Global Interactive Map Container Section -->
            <div class="lg:col-span-2 bg-slate-900/40 border border-slate-800 p-3 rounded-3xl shadow-2xl relative">
                <div id="map-canvas" class="rounded-2xl z-10"></div>
                <div class="absolute bottom-6 left-6 z-20 bg-slate-950/90 border border-slate-800 px-3 py-1.5 rounded-lg text-[11px] text-slate-400 shadow-md">
                    💡 <span class="text-slate-200">Interactive:</span> Click anywhere directly on the map to execute coordinate scans.
                </div>
            </div>
        </div>
    </div>

    <!-- Application Operational Architecture Pipeline Script -->
    <script>
        let geospatialMap = L.map('map-canvas').setView([20.296, 85.824], 5);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '© OpenStreetMap contributors © CARTO',
            subdomains: 'abcd',
            maxZoom: 19
        }).addTo(geospatialMap);

        let targetedActiveMarker = null;

        geospatialMap.on('click', function(event) {
            queryAtmosphericDatastream(event.latlng.lat, event.latlng.lng);
        });

        function executeManualQuery() {
            const latitude = document.getElementById('input-lat').value;
            const longitude = document.getElementById('input-lon').value;
            if (latitude && longitude) {
                queryAtmosphericDatastream(latitude, longitude);
            }
        }

        function triggerBrowserGeolocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        queryAtmosphericDatastream(position.coords.latitude, position.coords.longitude);
                    },
                    (error) => {
                        alert("Local telemetry check rejected: " + error.message);
                    }
                );
            } else {
                alert("This client browser lacks geolocation routing protocols.");
            }
        }

        async function queryAtmosphericDatastream(latitude, longitude) {
            document.getElementById('input-lat').value = parseFloat(latitude).toFixed(4);
            document.getElementById('input-lon').value = parseFloat(longitude).toFixed(4);

            geospatialMap.setView([latitude, longitude], 9);
            if (targetedActiveMarker) geospatialMap.removeLayer(targetedActiveMarker);
            targetedActiveMarker = L.marker([latitude, longitude]).addTo(geospatialMap);

            try {
                const streamResponse = await fetch(`http://127.0.0.1:8000/api/v1/pollution/lookup?lat=${latitude}&lon=${longitude}`);
                
                if (!streamResponse.ok) throw new Error("Target sector returning null telemetry.");
                const dataPayload = await streamResponse.json();
                
                const stats = dataPayload.metrics;
                const view = dataPayload.interpretation;

                document.getElementById('ui-station').innerText = dataPayload.meta.station_name;
                document.getElementById('ui-attribution').innerText = "Data feed from: " + dataPayload.meta.attribution;
                
                const aqiDisplay = document.getElementById('ui-aqi');
                aqiDisplay.innerText = stats.aqi;
                aqiDisplay.style.color = view.hex_color;

                const labelDisplay = document.getElementById('ui-interpretation');
                labelDisplay.innerText = view.label;
                labelDisplay.style.color = view.hex_color;

                document.getElementById('ui-hcho').innerText = stats.calculated_hcho_ppm + " ppm";
                
                const riskBadge = document.getElementById('ui-risk-badge');
                riskBadge.innerText = "Risk Level: " + view.hotspot_risk;
                riskBadge.className = `text-[10px] font-bold uppercase block mt-0.5 ${view.hotspot_risk === 'High Alert' ? 'text-red-400' : (view.hotspot_risk === 'Elevated' ? 'text-yellow-400' : 'text-slate-400')}`;

                document.getElementById('ui-pm25').innerText = stats.pm25 !== "N/A" ? stats.pm25 + " µg/m³" : "Offline";
                document.getElementById('ui-no2').innerText = stats.no2 !== "N/A" ? stats.no2 + " ppb" : "Offline";
                document.getElementById('ui-temp').innerText = stats.temperature !== "N/A" ? stats.temperature + " °C" : "Offline";

            } catch (err) {
                console.error("Critical parsing error: ", err);
                document.getElementById('ui-station').innerText = "Unmapped Coordinate Grid Zone";
                document.getElementById('ui-attribution').innerText = "Fallback tracking mode active.";
                document.getElementById('ui-aqi').innerText = "??";
                document.getElementById('ui-aqi').style.color = "#475569";
                document.getElementById('ui-interpretation').innerText = "No localized infrastructure detected.";
                document.getElementById('ui-interpretation').style.color = "#475569";
            }
        }
    </script>
</body>
</html>