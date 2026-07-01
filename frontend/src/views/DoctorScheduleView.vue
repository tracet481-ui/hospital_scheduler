<script setup>

    import { computed, ref } from "vue"

    const selectedDoctor = ref ("Dr. Ahmet")

    const doctors = [

        "Dr. Ahmet",
        "Dr. Mehmet",
        "Dr. Elif",
        "Dr. Can",

    ]


    const slots = []

    for (let hour = 8; hour < 18; hour ++) {

        slots.push(`${hour.toString().padStart(2,"0")}:00`)
        slots.push(`${hour.toString().padStart(2,"0")}:30`)

    }

    const days = [

        "Pazartesi",
        "Salı",
        "Çarşamba",
        "Perşembe",
        "Cuma",

    ]

</script>


<template>

    <div class = "container" >

        <aside class = "doctor-panel" >

            <h2>
                Doktorlar
            </h2>

            <div
                v-for = "doctor in doctors"
                key = "doctor"
                class = "doctor-card"
                @click = "selectedDoctor = doctor" >
            
            
                📁   {{ doctor }}
            
            </div>

        </aside>


        <main class = "calender-panel" >

            <h2>
                {{ selectedDoctor }}
            </h2>


            <table class = "calender">

                <thead>

                    <tr>

                        <th>
                            Saat
                        </th>

                        <th
                            v-for = "day in days"
                            key = "day">

                            {{ day }}

                        </th>

                    </tr>
                    
                </thead>


                <tbody>

                    <tr
                        v-for = "slot in slots"
                        key = "slot">

                        <td
                            class = "time">

                            {{ slot }}

                        </td>

                        <td
                            v-for = "day in days"
                            key = "day"
                            class = "empty">

                        </td>

                    </tr>

                </tbody>

            </table>

        </main>

    </div>

</template>


<style>

.container{
    display:flex;
    gap:20px;
    padding:20px;
}

.doctor-panel{
    width:250px;
    background:white;
    border-radius:12px;
    padding:20px;
    box-shadow:0 2px 8px rgba(0,0,0,.1);
}

.doctor-card{
    padding:15px;
    margin-bottom:10px;
    background:#f8fafc;
    border-radius:10px;
    cursor:pointer;
}

.doctor-card:hover{
    background:#e2e8f0;
}

.calendar-panel{
    flex:1;
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,.1);
}

.calendar{
    width:100%;
    border-collapse:collapse;
}

.calendar th{
    background:#f1f5f9;
    padding:12px;
}

.calendar td{
    border:1px solid #e2e8f0;
    height:40px;
    text-align:center;
}

.time{
    width:80px;
    font-weight:bold;
    background:#f8fafc;
}

.empty{
    background:white;
}

</style>