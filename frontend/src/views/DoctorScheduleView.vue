<script setup>

    import { computed, ref } from "vue"

    import { onMounted } from "vue"

    import { getLatestPlan } from "../services/scheduleApi"




    const selectedDoctor = ref ("Dr. Ahmet")

    const selectedDay = ref(15) 

    const doctors = [

        "Dr. Ahmet",
        "Dr. Mehmet",
        "Dr. Elif",
        "Dr. Can",
        "Dr. Ayşe",

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

    const appointments = ref([])





    const selectedDayName = computed (()  =>  {

        return weekDays[(selectedDay.value - 1) % 7 ]

    })

    const selectedAppointments = computed(() => {
        return appointments.value.filter((item) => {
            return (
                item.doctor?.trim() === selectedDoctor.value.trim() &&
                Number(item.day) === Number(selectedDay.value)
            )
        })
    })
    

    const normalizeTime = (time) => {
        if (!time) return ""

        return String(time)
            .replace(/\s/g, "")
            .slice(0, 5)
    }


    const timeToMinutes = (time) => {

        const normalized = normalizeTime(time)

        const [hour, minute] = normalized
            .split(":")
            .map(Number)

        return hour * 60 + minute
    }



    const getAppointmentForSlot = (slot) => {
        return selectedAppointments.value.find((item) => {
            return normalizeTime(item.time) === normalizeTime(slot)
        })
    }

      

    const getDayCount = (day) => {
        return appointments.value.filter((item) => {
            return (
                item.doctor?.trim() === selectedDoctor.value.trim() &&
                Number(item.day) === Number(day)
            )
        }).length
    }



    const getDayStatus =(day) => {

        if (getDayCount(day) > 0 )

            return "Plan"

    }





    const loadLatestPlan = async () => {

        try {

            const response = await getLatestPlan()

            const calendarMapping = {
                            0: 15,
                            1: 16,
                            2: 17,
                            3: 18,
                            4: 19,
                        }

            appointments.value = response.data.items.map((item) => ({
                doctor: item.surgeon?.trim(),
                day: calendarMapping[item.day_index],
                time: normalizeTime(item.start_time),
                end_time: normalizeTime(item.end_time),
                patient: item.patient,
                operation: item.operation,
                room: item.room,
                anesthesia: item.anesthesia_team,
                status: "Planlandı",
            }))



                // console.log ("appointments", appointments.value)
                // console.log ("selectedDoctor", selectedDoctor.value)
                // console.log ("selectedDay", selectedDay.value)
                // console.log ("selectedAppointments", selectedAppointments.value)

        }   catch (error) {

            console.log (error)

        }
    }

    onMounted (
        () => {

            loadLatestPlan()
            
        }
    
    )

    const slotRows = computed(() => {
        return slots.map((slot) => {
            const slotMinute = timeToMinutes(slot)

            const appointment = selectedAppointments.value.find((item) => {
                const start = timeToMinutes(item.time)
                const end = timeToMinutes(item.end_time)

                return slotMinute >= start && slotMinute < end
            })

            return {
                slot,
                appointment,
            }
        })
    })

</script>



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
                        v-if="getDayStatus(day)"
                        class="day-button create"
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
                        v-for="row in slotRows"
                        :key="row.slot"
                        :class="{
                            filled: row.appointment,
                            done: row.appointment?.status === 'Tamamlandı',
                        }"
                    >
                        <td class="time-cell">{{ row.slot }}</td>

            

                        <template v-if="row.appointment">
                            <td>{{ row.appointment.patient }}</td>
                            <td>{{ row.appointment.operation }}</td>
                            <td>{{ row.appointment.room }}</td>
                            <td>{{ row.appointment.anesthesia }}</td>
                            <td>
                                <span class="status-badge planned">
                                    {{ row.appointment.status }}
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