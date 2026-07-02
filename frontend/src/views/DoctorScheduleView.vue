<script setup>

    import { computed, ref } from "vue"

    const selectedDoctor = ref ("Dr. Ahmet")

    const selectedDay = ref(15) 

    const doctors = [

        "Dr. Ahmet",
        "Dr. Mehmet",
        "Dr. Elif",
        "Dr. Can",

    ]



    // for (let hour = 8; hour < 18; hour ++) {

    //     slots.push(`${hour.toString().padStart(2,"0")}:00`)
    //     slots.push(`${hour.toString().padStart(2,"0")}:30`)

    // }

    const weekDays = [

        "Pazartesi",
        "Salı",
        "Çarşamba",
        "Perşembe",
        "Cuma",
        "Cumartesi",
        "Pazar",

    ]

    const calendarDays = Array.from ({ length: 31 }, (_, index) => index + 1)

    const slots = []

    for ( let hour = 8 ; hour < 18 ; hour ++) {

        const h = hour.toString().padStart(2, "0")

        slots.push (`${h}:00`)
        slots.push (`${h}:30`)

    }

    const appointments = [


    {
        doctor: "Dr. Ahmet",
        day: 15,
        time: "08:00",
        patient: "P12 - Ayşe Yılmaz",
        operation: "Katarakt Ameliyatı",
        room: "OR-1",
        anesthesia: "Team-A",
        status: "Planlandı",
    },
    {
        doctor: "Dr. Ahmet",
        day: 15,
        time: "09:00",
        patient: "P18 - Mehmet Demir",
        operation: "Diz Artroskopisi",
        room: "OR-2",
        anesthesia: "Team-B",
        status: "Planlandı",
    },
    {
        doctor: "Dr. Ahmet",
        day: 15,
        time: "11:00",
        patient: "P27 - Fatma Şahin",
        operation: "Safra Kesesi Ameliyatı",
        room: "OR-3",
        anesthesia: "Team-C",
        status: "Tamamlandı",
    },
 

    ]


    const selectedDayName = computed (()  =>  {

        return weekDays[(selectedDay.value - 1) % 7 ]

    })

    const selectedAppointments = computed(() => {
        return appointments.filter(
            ( item )  => {
                return item.doctor === selectedDoctor.value &&
                    item.day === selectedDay.value
                    })
    })
    


    const getAppointmentForSlot = (slot) => {

        return selectedAppointments.value.find (

            (item) => item.time === slot

    )}

      

    const getDayCount = (day) => {

        return appointments.filter (

            (item) => {
                return item.doctor === selectedDoctor.value &&
                item.day === day
                
            
            }).length

    }

    const getDayStatus = (day) => {

        if (day < 15)   return "Geçmiş"
        if (day <= 31)  return "Oluştur"

        return "Pasif"

    }




</script>


<!-- <template>

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

</template> -->


<template>
    <main class="doctor-page">
        <section class="top-title">
            <div>
                <h1>Doktor Takvimleri</h1>
                <p>Hastane Yönetim Sistemi</p>
            </div>

            <select v-model="selectedDoctor">
                <option v-for="doctor in doctors" :key="doctor" :value="doctor">
                    {{ doctor }}
                </option>
            </select>
        </section>

        <section class="calendar-card">
            <h2>Takvimden Randevu Oluştur</h2>

            <div class="month-bar">
                <button>Geçmiş Ay</button>
                <h3>Temmuz 2026</h3>
                <button>Gelecek Ay</button>
            </div>

            <div class="calendar-grid">
                <div v-for="dayName in weekDays" :key="dayName" class="calendar-head">
                    {{ dayName }}
                </div>

                <div
                    v-for="day in calendarDays"
                    :key="day"
                    class="calendar-cell"
                    :class="{ selected: selectedDay === day }"
                    @click="selectedDay = day"
                >
                    <span class="day-number">{{ day }}</span>

                    <button
                        class="day-button"
                        :class="getDayStatus(day) === 'Geçmiş' ? 'past' : 'create'"
                    >
                        {{ getDayStatus(day) }}
                    </button>

                    <span v-if="getDayCount(day)" class="count-badge">
                        {{ getDayCount(day) }}
                    </span>
                </div>
            </div>
        </section>

        <section class="schedule-card">
            <div class="schedule-title">
                <h2>
                    {{ selectedDay }} Temmuz 2026 -
                    {{ selectedDayName }} |
                    {{ selectedDoctor }}
                </h2>

                <button class="add-btn">+ Randevu Ekle</button>
            </div>

            <table class="slot-table">
                <thead>
                    <tr>
                        <th>Saat</th>
                        <th>Hasta</th>
                        <th>Ameliyat</th>
                        <th>Oda</th>
                        <th>Anestezi Ekibi</th>
                        <th>Durum</th>
                        <th>İşlemler</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="slot in slots"
                        :key="slot"
                        :class="{
                            filled: getAppointmentForSlot(slot),
                            done: getAppointmentForSlot(slot)?.status === 'Tamamlandı',
                            // breakrow: slot === '12:00' || slot === '12:30'
                        }"
                    >
                        <td class="time-cell">{{ slot }}</td>

                        <template v-if="slot === '12:00' || slot === '12:30'">
                            <td colspan="6" class="break-cell">MOLA</td>
                        </template>

                        <template v-else-if="getAppointmentForSlot(slot)">
                            <td>{{ getAppointmentForSlot(slot).patient }}</td>
                            <td>{{ getAppointmentForSlot(slot).operation }}</td>
                            <td>{{ getAppointmentForSlot(slot).room }}</td>
                            <td>{{ getAppointmentForSlot(slot).anesthesia }}</td>
                            <td>
                                <span
                                    class="status-badge"
                                    :class="getAppointmentForSlot(slot).status === 'Tamamlandı' ? 'success' : 'planned'"
                                >
                                    {{ getAppointmentForSlot(slot).status }}
                                </span>
                            </td>
                            <td class="actions">👁 🗑</td>
                        </template>

                        <template v-else>
                            <td colspan="6" class="empty-cell"></td>
                        </template>
                    </tr>
                </tbody>
            </table>
        </section>
    </main>
</template>




<!-- 
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

</style> -->




<style scoped>
.doctor-page {
    min-height: 100vh;
    background: #eef3f8;
    padding: 24px;
    color: #18233f;
}

.top-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.top-title h1 {
    color: #12305a;
    font-size: 28px;
}

.top-title p {
    color: #64748b;
    margin-top: 4px;
}

.top-title select {
    min-width: 220px;
    padding: 12px;
    border: 1px solid #d8e0ec;
    border-radius: 8px;
    background: white;
}

.calendar-card,
.schedule-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 22px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
}

.calendar-card h2 {
    color: #5b35b1;
    font-size: 20px;
    margin-bottom: 16px;
}

.month-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 28px;
    margin-bottom: 18px;
}

.month-bar h3 {
    font-size: 28px;
    color: #1e293b;
}

.month-bar button,
.add-btn {
    background: #6d44c6;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 22px;
    cursor: pointer;
    box-shadow: 0 6px 12px rgba(109, 68, 198, 0.25);
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    border: 1px solid #dde5ef;
}

.calendar-head {
    padding: 14px;
    text-align: center;
    font-weight: 700;
    background: #fbfdff;
    border-right: 1px solid #dde5ef;
    border-bottom: 1px solid #dde5ef;
}

.calendar-cell {
    position: relative;
    min-height: 92px;
    padding: 12px;
    border-right: 1px solid #dde5ef;
    border-bottom: 1px solid #dde5ef;
    background: white;
    cursor: pointer;
}

.calendar-cell.selected {
    background: #fffeca;
}

.day-number {
    font-size: 16px;
    color: #1e293b;
}

.day-button {
    position: absolute;
    left: 50%;
    bottom: 14px;
    transform: translateX(-50%);
    border: none;
    border-radius: 4px;
    color: white;
    padding: 8px 18px;
    cursor: pointer;
}

.day-button.create {
    background: #10b993;
    box-shadow: 0 6px 12px rgba(16, 185, 147, 0.3);
}

.day-button.past {
    background: #17203d;
    box-shadow: 0 6px 12px rgba(23, 32, 61, 0.25);
}

.count-badge {
    position: absolute;
    right: 30%;
    bottom: 42px;
    background: #2687ff;
    color: white;
    border-radius: 50%;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 700;
}

.schedule-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.schedule-title h2 {
    color: #5b35b1;
    font-size: 22px;
}

.slot-table {
    width: 100%;
    border-collapse: collapse;
}

.slot-table th,
.slot-table td {
    border-bottom: 1px solid #e5edf5;
    padding: 9px 12px;
    text-align: left;
}

.slot-table th {
    background: #fbfdff;
    color: #26324f;
    font-weight: 700;
}

.time-cell {
    width: 90px;
    font-weight: 600;
}

.filled {
    background: #f3e9f8;
}

.done {
    background: #e9f8ee;
}

.breakrow {
    background: #fff7c7;
}

.break-cell {
    text-align: center;
    font-weight: 700;
    color: #334155;
}

.empty-cell {
    height: 28px;
}

.status-badge {
    padding: 5px 12px;
    border-radius: 6px;
    font-weight: 700;
}

.status-badge.planned {
    background: #e6d7ff;
    color: #5b35b1;
}

.status-badge.success {
    background: #c9f4d7;
    color: #148843;
}

.actions {
    text-align: center;
}
</style>