package org.study.notes;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import org.json.JSONArray;
import java.util.ArrayList;

public class MainActivity extends Activity {
    private final ArrayList<String> notes = new ArrayList<>();
    private EditText input;
    private TextView error;
    private TextView count;
    private LinearLayout list;
    private SharedPreferences preferences;

    private int dp(int value) { return (int)(getResources().getDisplayMetrics().density * value); }

    private TextView text(String value, int size, int color) {
        TextView view = new TextView(this);
        view.setText(value); view.setTextSize(size); view.setTextColor(color);
        view.setPadding(0, dp(6), 0, dp(6));
        return view;
    }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        preferences = getSharedPreferences("notes", MODE_PRIVATE);
        try {
            JSONArray saved = new JSONArray(preferences.getString("items", "[]"));
            for (int i=0; i<saved.length(); i++) notes.add(saved.getString(i));
        } catch (Exception ignored) { }
        getWindow().setStatusBarColor(Color.rgb(19,45,70));
        getWindow().setNavigationBarColor(Color.rgb(19,45,70));
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(22), dp(18), dp(22), dp(10));
        root.setBackgroundColor(Color.rgb(238,243,247));
        root.addView(text("ЛАБОРАТОРНАЯ РАБОТА 07",12,Color.rgb(17,108,103)));
        root.addView(text("Мои заметки",30,Color.rgb(19,45,70)));
        root.addView(text("Добавляйте важное. Заметки сохраняются на устройстве.",14,Color.rgb(85,105,125)));
        input = new EditText(this);
        input.setId(1001);
        input.setContentDescription("note_input");
        input.setHint("Текст новой заметки"); input.setMinLines(1); input.setMaxLines(3);
        input.setTextSize(16);
        input.setText(state != null ? state.getString("draft", "") : preferences.getString("draft", ""));
        root.addView(input, new LinearLayout.LayoutParams(-1,-2));
        Button add = new Button(this);
        add.setContentDescription("add_note"); add.setText("Добавить заметку");
        add.setAllCaps(false); add.setTextColor(Color.WHITE);
        add.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(17,108,103)));
        root.addView(add, new LinearLayout.LayoutParams(-1,dp(52)));
        error = text("",14,Color.rgb(161,43,52)); error.setContentDescription("note_error");
        root.addView(error);
        count = text("",14,Color.rgb(85,105,125)); count.setContentDescription("note_count");
        root.addView(count);
        ScrollView scroll = new ScrollView(this); scroll.setContentDescription("notes_scroll");
        list = new LinearLayout(this); list.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(list);
        root.addView(scroll, new LinearLayout.LayoutParams(-1,0,1));
        setContentView(root);
        add.setOnClickListener(view -> {
            String value = input.getText().toString().trim();
            if (value.isEmpty()) {error.setText("Введите текст заметки"); return;}
            notes.add(value); input.setText(""); error.setText(""); save(); render();
            ((InputMethodManager)getSystemService(INPUT_METHOD_SERVICE)).hideSoftInputFromWindow(input.getWindowToken(),0);
            input.clearFocus();
        });
        render();
    }

    private void render() {
        list.removeAllViews(); count.setText("Заметок: " + notes.size());
        if (notes.isEmpty()) list.addView(text("Пока нет заметок",17,Color.rgb(85,105,125)));
        for (int i=0; i<notes.size(); i++) {
            final int index = i;
            LinearLayout row = new LinearLayout(this); row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(dp(12),dp(8),dp(6),dp(8)); row.setBackgroundColor(Color.WHITE);
            LinearLayout.LayoutParams rowParams = new LinearLayout.LayoutParams(-1,-2); rowParams.bottomMargin=dp(10);
            TextView title = text(notes.get(i),17,Color.rgb(19,45,70)); title.setContentDescription("note_"+i);
            row.addView(title,new LinearLayout.LayoutParams(0,-2,1));
            Button remove = new Button(this); remove.setText("×"); remove.setTextSize(22);
            remove.setContentDescription("delete_note_"+i);
            remove.setOnClickListener(view -> {notes.remove(index); save(); render();});
            row.addView(remove,new LinearLayout.LayoutParams(dp(52),dp(48)));
            list.addView(row,rowParams);
        }
    }

    private void save() {
        JSONArray data = new JSONArray(); for (String note: notes) data.put(note);
        preferences.edit().putString("items",data.toString()).putString("draft",input.getText().toString()).commit();
    }
    @Override protected void onPause() {super.onPause(); save();}
    @Override public void onSaveInstanceState(Bundle state) {
        state.putString("draft",input.getText().toString()); super.onSaveInstanceState(state);
    }
}
