# CSS Enhancement Reference

MiiBrowser now includes enhanced CSS support through automatic injection. The following styles and utility classes are available:

## 🎨 Color Utilities

### Text Colors

```html
<p class="text-primary">Primary blue text</p>
<p class="text-secondary">Secondary gray text</p>
<p class="text-success">Success green text</p>
<p class="text-danger">Danger red text</p>
<p class="text-warning">Warning yellow text</p>
<p class="text-info">Info cyan text</p>
<p class="text-light">Light gray text</p>
<p class="text-dark">Dark text</p>
<p class="text-white">White text</p>
<p class="text-muted">Muted gray text</p>
```

### Background Colors

```html
<div class="bg-primary">Primary blue background</div>
<div class="bg-secondary">Secondary gray background</div>
<div class="bg-success">Success green background</div>
<div class="bg-danger">Danger red background</div>
<div class="bg-warning">Warning yellow background</div>
<div class="bg-info">Info cyan background</div>
<div class="bg-light">Light gray background</div>
<div class="bg-dark">Dark background</div>
<div class="bg-white">White background</div>
```

## 📏 Width and Height

### Width Utilities

```html
<div class="w-25">25% width</div>
<div class="w-50">50% width</div>
<div class="w-75">75% width</div>
<div class="w-100">100% width</div>
<div class="w-auto">Auto width</div>
```

### Height Utilities

```html
<div class="h-25">25% height</div>
<div class="h-50">50% height</div>
<div class="h-75">75% height</div>
<div class="h-100">100% height</div>
<div class="h-auto">Auto height</div>
```

## 📍 Positioning

### Position Types

```html
<div class="position-static">Static position (default)</div>
<div class="position-relative">Relative position</div>
<div class="position-absolute">Absolute position</div>
<div class="position-fixed">Fixed position</div>
<div class="position-sticky">Sticky position</div>
```

### Z-Index Layers

```html
<div class="z-index-0">Layer 0 (bottom)</div>
<div class="z-index-10">Layer 10</div>
<div class="z-index-100">Layer 100</div>
<div class="z-index-1000">Layer 1000 (top)</div>
```

## 📦 Spacing

### Margin Utilities

```html
<div class="m-0">No margin</div>
<div class="m-1">Margin 0.25rem</div>
<div class="m-2">Margin 0.5rem</div>
<div class="m-3">Margin 1rem</div>
<div class="m-4">Margin 1.5rem</div>
<div class="m-5">Margin 3rem</div>
<div class="m-auto">Auto margin</div>

<!-- Directional margins -->
<div class="mt-3">Margin top</div>
<div class="mb-3">Margin bottom</div>
<div class="ml-3">Margin left</div>
<div class="mr-3">Margin right</div>
<div class="mx-3">Margin left and right</div>
<div class="my-3">Margin top and bottom</div>
```

### Padding Utilities

```html
<div class="p-0">No padding</div>
<div class="p-1">Padding 0.25rem</div>
<div class="p-2">Padding 0.5rem</div>
<div class="p-3">Padding 1rem</div>
<div class="p-4">Padding 1.5rem</div>
<div class="p-5">Padding 3rem</div>

<!-- Directional padding -->
<div class="pt-3">Padding top</div>
<div class="pb-3">Padding bottom</div>
<div class="pl-3">Padding left</div>
<div class="pr-3">Padding right</div>
<div class="px-3">Padding left and right</div>
<div class="py-3">Padding top and bottom</div>
```

## 📝 Text Alignment

```html
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>
<p class="text-justify">Justified</p>
```

## 🎭 Opacity

```html
<div class="opacity-0">0% opacity (invisible)</div>
<div class="opacity-25">25% opacity</div>
<div class="opacity-50">50% opacity</div>
<div class="opacity-75">75% opacity</div>
<div class="opacity-100">100% opacity (fully visible)</div>
```

## 🎯 Display

```html
<div class="d-none">Hidden</div>
<div class="d-block">Block display</div>
<div class="d-inline">Inline display</div>
<div class="d-inline-block">Inline-block display</div>
<div class="d-flex">Flex display</div>
```

## 🖼️ Borders and Rounded Corners

### Borders

```html
<div class="border">All borders</div>
<div class="border-top">Top border</div>
<div class="border-bottom">Bottom border</div>
<div class="border-left">Left border</div>
<div class="border-right">Right border</div>
<div class="border-0">No border</div>
```

### Rounded Corners

```html
<div class="rounded">Rounded corners (0.25rem)</div>
<div class="rounded-sm">Small rounded (0.2rem)</div>
<div class="rounded-lg">Large rounded (0.5rem)</div>
<div class="rounded-circle">Circle</div>
<div class="rounded-0">No rounding</div>
```

## 🌊 Overflow

```html
<div class="overflow-auto">Auto overflow</div>
<div class="overflow-hidden">Hidden overflow</div>
<div class="overflow-visible">Visible overflow</div>
<div class="overflow-scroll">Scrollable overflow</div>
```

## 📊 Common Components

### Buttons

```html
<button class="btn">Default button</button>
```

### Links

```html
<a href="#" class="link">Enhanced link</a>
```

### Tables

Tables automatically get styled with borders and padding:

```html
<table>
	<thead>
		<tr><th>Header</th></tr>
	</thead>
	<tbody>
		<tr><td>Cell</td></tr>
	</tbody>
</table>
```

### Images

```html
<img src="..." class="img-fluid" alt="..." />
```

## 💡 Inline CSS Support

You can also use inline styles:

```html
<div
	style="color: red; background-color: yellow; width: 50%; height: 100px; position: relative; z-index: 10;"
>
	Custom inline styles
</div>
```

## ⚠️ Known Limitations

While MiiBrowser enhances CSS support, some advanced features may not work due to tkinterweb limitations:

- Complex CSS3 features (flexbox, grid, transforms)
- Advanced animations and transitions
- Shadow DOM
- Complex pseudo-selectors

For best results, use:

- Basic colors and backgrounds
- Simple positioning (relative, absolute, fixed)
- Width and height (%, px, rem)
- Z-index for layering
- Margin and padding
- Borders and border-radius

## 🧪 Testing

Run the CSS demo to see all features in action:

```bash
python examples/test_css_demo.py
```

Or open the test file directly:

```bash
python -m miibrowser examples/css_test.html
```

## 🔧 How It Works

MiiBrowser automatically injects enhanced CSS into every page you load:

1. Fetches the HTML content
2. Injects 7.5KB of enhanced CSS into the `<head>`
3. Loads the enhanced HTML in the embedded browser
4. Falls back to direct loading if injection fails

This provides much better styling support while keeping the embedded browser architecture.
