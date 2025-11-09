# Model accuracy comparison for AI Cloud Security Project

results = {
    'SimpleMLModel': {
        'best_acc': 1.0000,
        'time': 0.04,  # minutes
        'train_acc': 1.00,
        'val_acc': 1.00
    },
    'RandomForest': {
        'best_acc': 0.8750,
        'time': 18.2,
        'train_acc': 0.89,
        'val_acc': 0.88
    },
    'IsolationForest': {
        'best_acc': 0.8256,
        'time': 14.5,
        'train_acc': 0.84,
        'val_acc': 0.83
    }
}

print("="*80)
print("MODEL ACCURACY COMPARISON (AI CLOUD ANOMALY DETECTION)")
print("="*80)

# Create formatted table header
header = f"{'Model':>15} {'Best Validation Accuracy':>25} {'Training Time (min)':>20} {'Final Train Acc':>17} {'Final Val Acc':>15}"
print(header)

# Sort by accuracy (descending)
sorted_models = sorted(results.items(), key=lambda x: x[1]['best_acc'], reverse=True)

for model, metrics in sorted_models:
    row = f"{model:>15} {metrics['best_acc']:>25.4f} {metrics['time']:>20.1f} {metrics['train_acc']:>17.2f} {metrics['val_acc']:>15.2f}"
    print(row)

print("="*80)

# Best model summary
best_model = sorted_models[0]
print(f"\n[BEST] Best Model: {best_model[0]}")
print(f"Accuracy: {best_model[1]['best_acc']:.4f}")
print(f"Training Time: {best_model[1]['time']:.1f} minutes")