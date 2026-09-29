"""Runs in the GitHub build after `cap add android`.
Makes the status bar AND the navigation bar fully transparent (edge-to-edge)
and passes the real system-bar heights to the web page."""
import pathlib, re

root = pathlib.Path("android/app/src/main")

# 1) MainActivity.java
main = next(root.glob("java/**/MainActivity.java"))
pkg = re.search(r"^package\s+([\w.]+);", main.read_text(), re.M).group(1)
main.write_text('''package %s;

import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.WebViewListener;

public class MainActivity extends BridgeActivity {
  private volatile float topDp = 0f;
  private volatile float bottomDp = 0f;

  public class InsetsBridge {
    @JavascriptInterface public float getTop() { return topDp; }
    @JavascriptInterface public float getBottom() { return bottomDp; }
    @JavascriptInterface public void setLightBars(final boolean light) {
      runOnUiThread(() -> {
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        c.setAppearanceLightStatusBars(light);
        c.setAppearanceLightNavigationBars(light);
      });
    }
  }

  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
    getWindow().setStatusBarColor(Color.TRANSPARENT);
    getWindow().setNavigationBarColor(Color.TRANSPARENT);
    if (Build.VERSION.SDK_INT >= 29) {
      getWindow().setNavigationBarContrastEnforced(false);
    }
    final WebView wv = getBridge().getWebView();
    wv.addJavascriptInterface(new InsetsBridge(), "AndroidInsets");
    ViewCompat.setOnApplyWindowInsetsListener(wv, (v, insets) -> {
      Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());
      Insets ime = insets.getInsets(WindowInsetsCompat.Type.ime());
      float d = getResources().getDisplayMetrics().density;
      topDp = bars.top / d;
      bottomDp = Math.max(bars.bottom, ime.bottom) / d;
      pushInsets(wv);
      return insets;
    });
    getBridge().addWebViewListener(new WebViewListener() {
      @Override public void onPageLoaded(WebView view) { pushInsets(view); }
    });
    ViewCompat.requestApplyInsets(wv);
  }

  private void pushInsets(final WebView wv) {
    final String js = "(function(){var s=document.documentElement.style;"
      + "s.setProperty('--native-sat','" + topDp + "px');"
      + "s.setProperty('--native-sab','" + bottomDp + "px');})();";
    wv.post(() -> wv.evaluateJavascript(js, null));
  }
}
''' % pkg)

# 2) theme: transparent bars + draw behind cutout
styles = root / "res/values/styles.xml"
x = styles.read_text()
items = '''
        <item name="android:statusBarColor">@android:color/transparent</item>
        <item name="android:navigationBarColor">@android:color/transparent</item>
        <item name="android:windowDrawsSystemBarBackgrounds">true</item>
        <item name="android:windowLayoutInDisplayCutoutMode">shortEdges</item>
    '''
x = re.sub(r'(<style name="AppTheme\.NoActionBar"[^>]*>)(.*?)(</style>)',
           lambda m: m.group(1) + m.group(2) + items + m.group(3), x, count=1, flags=re.S)
styles.write_text(x)
print("patched", main, styles)
