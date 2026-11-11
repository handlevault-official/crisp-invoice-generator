// text-db.js - Simple Text-Based Offline Database para sa Terracotta App
const TextDB = {
    DB_KEY: 'terracotta_text_database_v1',

    // I-initialize ang database kung wala pa
    init: function() {
        if (!localStorage.getItem(this.DB_KEY)) {
            const initialData = {
                logs: [],
                notes: [],
                patients: []
            };
            localStorage.setItem(this.DB_KEY, JSON.stringify(initialData));
            console.log("[TextDB] Initialized new text-based database.");
        }
    },

    // Kunin ang buong database
    getAll: function() {
        this.init();
        try {
            return JSON.parse(localStorage.getItem(this.DB_KEY));
        } catch (e) {
            console.error("[TextDB] Error reading database:", e);
            return { logs: [], notes: [], patients: [] };
        }
    },

    // Magdagdag ng bagong text log (Halimbawa: Voice logs o Vitals)
    addLog: function(category, textContent, nurseId = 'Nurse-On-Duty') {
        const db = this.getAll();
        const newEntry = {
            id: 'LOG_' + Date.now(),
            timestamp: new Date().toLocaleString(),
            category: category,
            content: textContent,
            nurse: nurseId
        };
        db.logs.unshift(newEntry); // Ilalagay sa unahan
        localStorage.setItem(this.DB_KEY, JSON.stringify(db));
        console.log("[TextDB] Log added successfully:", newEntry);
        return newEntry;
    },

    // Mag-save ng shift text note
    addNote: function(noteTitle, noteBody) {
        const db = this.getAll();
        const newNote = {
            id: 'NOTE_' + Date.now(),
            date: new Date().toLocaleDateString(),
            title: noteTitle,
            body: noteBody
        };
        db.notes.unshift(newNote);
        localStorage.setItem(this.DB_KEY, JSON.stringify(db));
        return newNote;
    },

    // I-export ang buong database bilang Text / JSON file para sa backup
    exportAsTextFile: function() {
        const data = JSON.stringify(this.getAll(), null, 2);
        const blob = new Blob([data], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Terracotta_Shift_DB_${Date.now()}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    },

    // Burahin ang database (Reset)
    clearDB: function() {
        localStorage.removeItem(this.DB_KEY);
        this.init();
        console.log("[TextDB] Database cleared and re-initialized.");
    }
};

// Auto-initialize kapag nag-load
document.addEventListener('DOMContentLoaded', () => {
    TextDB.init();
});

Object.freeze(TextDB);
